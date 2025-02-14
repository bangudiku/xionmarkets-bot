import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# **1️⃣ Setup Selenium**
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# **2️⃣ Buka XionMarkets Testnet**
driver.get("https://testnet.xionmarkets.com")

# **3️⃣ Tunggu halaman benar-benar terbuka sebelum lanjut**
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ Halaman utama berhasil dimuat!")
except Exception as e:
    print(f"❌ Gagal memuat halaman utama: {e}")
    driver.quit()

# **4️⃣ Load Local Storage Data untuk Login Otomatis**
with open("config.json", "r") as f:
    local_storage_data = json.load(f)

# **5️⃣ Masukkan Local Storage ke Selenium**
for key, value in local_storage_data.items():
    driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")

print("✅ Local Storage berhasil dimasukkan!")

# **6️⃣ Refresh Halaman untuk Login Otomatis**
driver.refresh()

# **7️⃣ Tunggu hingga elemen tertentu muncul setelah login**
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]'))
    )
    print("✅ Login otomatis selesai! Halaman siap!")
except Exception as e:
    print(f"❌ Gagal login otomatis: {e}")
    driver.quit()

# **8️⃣ Navigasi ke Halaman Market**
market_url = "https://testnet.xionmarkets.com/market/xion1x89jut7kersq6nws063v2wdnl5l468j0vrpzxh0d7ezv0f9yn4qshyatss/1"
driver.get(market_url)

# **9️⃣ Tunggu halaman market benar-benar terbuka**
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="trade"]'))
    )
    print("✅ Halaman market berhasil dimuat!")
except Exception as e:
    print(f"❌ Gagal memuat halaman market: {e}")
    driver.quit()

def get_balance():
    """Mengambil saldo pengguna."""
    try:
        balance_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="trade"]/div[3]/div/span[2]'))
        )
        balance_text = balance_element.text.replace(',', '')  # Hilangkan koma
        balance = float(balance_text)
        print(f"💰 Saldo saat ini: {balance} USDC")
        return balance
    except Exception as e:
        print(f"❌ Gagal mendapatkan saldo: {e}")
        return 0

def wait_for_transaction():
    """Menunggu hingga transaksi berhasil atau timeout dalam 60 detik."""
    print("⏳ Menunggu transaksi dikirim...")
    try:
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.XPATH, "//*[@id='root']"), "Transaction submitted. Waiting for confirmation...")
        )
        print("✅ Transaksi dikirim, menunggu konfirmasi...")

        timeout = time.time() + 60  # Timeout 60 detik
        while time.time() < timeout:
            try:
                confirmation_text = driver.find_element(By.XPATH, "//*[@id='root']").text
                if "Transaction completed. You have bought No share(s) successfully!" in confirmation_text:
                    print("🎉 Transaksi selesai! Lanjut ke trade berikutnya...")
                    return True
            except Exception:
                pass  # Jika elemen tidak ditemukan, lanjutkan loop
            time.sleep(5)  # Tunggu 5 detik sebelum cek ulang
        else:
            print("⚠️ Transaksi terlalu lama, halaman akan direfresh...")
            driver.refresh()
            time.sleep(5)
            return False
    except Exception as e:
        print(f"⚠️ Terjadi kesalahan saat menunggu transaksi: {e}")
        driver.refresh()
        time.sleep(5)
        return False

# Klik tombol "No" sebelum buy jika ada pop-up
try:
    no_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="trade"]/div[2]/button[2]'))
    )
    no_button.click()
    print("✅ Klik 'No' berhasil!")
    time.sleep(2)
except Exception:
    print("ℹ️ Tidak ada tombol 'No', lanjutkan proses...")

# **🔄 10️⃣ Loop Auto Buy**
while True:
    try:
        balance = get_balance()
        if balance < 1:
            print("❌ Saldo tidak cukup untuk membeli! Menunggu 30 detik sebelum cek ulang...")
            time.sleep(30)
            continue

        # Masukkan jumlah USDC yang mau dibeli
        buy_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="buy-input"]'))
        )
        buy_input.clear()
        buy_input.send_keys("1")  # Masukkan jumlah 1 USDC
        time.sleep(1)

        # Klik tombol "Buy"
        buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="trade"]/div[6]/button'))
        )
        buy_button.click()
        time.sleep(2)

        # Klik tombol "Confirm action"
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[1]/div/div[2]/div[3]/button'))
        )
        confirm_button.click()
        print("✅ Order berhasil dieksekusi!")

        # Tunggu transaksi selesai sebelum lanjut
        if wait_for_transaction():
            print("✅ Siap melakukan pembelian berikutnya...")
        else:
            print("⚠️ Terjadi masalah, akan mencoba lagi...")

    except Exception as e:
        print(f"❌ Error dalam loop utama: {e}")
        time.sleep(5)  # Tunggu sebelum mencoba ulang
