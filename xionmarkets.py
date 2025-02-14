import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# **1️⃣ Setup Selenium**
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# **2️⃣ Buka XionMarkets Testnet**
driver.get("https://testnet.xionmarkets.com")
time.sleep(3)  # Tunggu halaman terbuka

# **3️⃣ Local Storage Data (untuk Login Otomatis)**
with open("config.json", "r") as f:
    local_storage_data = json.load(f)

# **4️⃣ Masukkan Local Storage ke Selenium**
for key, value in local_storage_data.items():
    driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")

print("✅ Local Storage berhasil dimasukkan!")

# **5️⃣ Refresh Halaman untuk Login Otomatis**
driver.refresh()
time.sleep(5)

print("✅ Login otomatis selesai!")

# **6️⃣ Navigasi ke Halaman Market untuk Auto Buy**
market_url = "https://testnet.xionmarkets.com/market/xion1x89jut7kersq6nws063v2wdnl5l468j0vrpzxh0d7ezv0f9yn4qshyatss/1"
driver.get(market_url)
time.sleep(5)

def get_balance():
    try:
        balance_element = driver.find_element(By.XPATH, '//*[@id="trade"]/div[3]/div/span[2]')  # XPath hasil record
        balance_text = balance_element.text.replace(',', '')  # Hilangkan koma
        balance = float(balance_text)
        print(f"💰 Saldo saat ini: {balance} USDC")
        return balance
    except Exception as e:
        print(f"❌ Gagal mendapatkan saldo: {e}")
        return 0

# Klik tombol "No" sebelum buy
try:
    no_button = driver.find_element(By.XPATH, '//*[@id="trade"]/div[2]/button[2]')
    no_button.click()
    print("✅ Klik 'No' berhasil!")
    time.sleep(2)  # Tunggu sebentar sebelum lanjut ke Buy
except Exception as e:
    print(f"❌ Gagal klik 'No': {e}")

# **7️⃣ Loop Auto Buy**
while True:
    try:
        balance = get_balance()
        if balance < 1:
            print("❌ Saldo tidak cukup untuk membeli!")
            time.sleep(10)
            continue

        # Masukkan jumlah USDC yang mau dibeli
        buy_input = driver.find_element(By.XPATH, '//*[@id="buy-input"]')
        buy_input.clear()
        buy_input.send_keys("1")  # Masukkan jumlah 1 USDC
        time.sleep(1)

        # Klik tombol "Buy"
        buy_button = driver.find_element(By.XPATH, '//*[@id="trade"]/div[6]/button')
        buy_button.click()
        time.sleep(2)

        # Klik tombol "Confirm action"
        confirm_button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div[1]/div/div[2]/div[3]/button')
        confirm_button.click()
        print("✅ Order berhasil dieksekusi!")

        # 🔄 **Menunggu transaksi dikirim (maks 30 detik)**
        try:
            print("⏳ Menunggu transaksi dikirim...")
            WebDriverWait(driver, 30).until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[@id='root']"), "Transaction submitted. Waiting for confirmation...")
            )
            print("✅ Transaksi dikirim, menunggu konfirmasi...")

            # 🔄 **Loop cek transaksi hingga dikonfirmasi atau timeout 60 detik**
            timeout = time.time() + 60  # 60 detik timeout
            while time.time() < timeout:
                try:
                    confirmation_text = driver.find_element(By.XPATH, "//*[@id='root']").text
                    if "Transaction completed" in confirmation_text:
                        print("🎉 Transaksi selesai! Lanjut ke trade berikutnya...")
                        break  # Keluar dari loop jika transaksi sukses
                except Exception:
                    pass  # Jika elemen tidak ditemukan, lanjutkan loop
                time.sleep(5)  # Tunggu 5 detik sebelum cek ulang
            else:
                print("⚠️ Transaksi terlalu lama, halaman akan direfresh...")
                driver.refresh()  # 🔄 **Refresh halaman**
                time.sleep(5)  # Tunggu 5 detik sebelum mencoba lagi

        except Exception as e:
            print("⚠️ Transaksi tidak terkirim dalam 30 detik, halaman akan direfresh...")
            driver.refresh()  # 🔄 **Refresh halaman**
            time.sleep(5)  # Tunggu 5 detik sebelum mencoba lagi

    except Exception as e:
        print(f"❌ Error dalam loop utama: {e}")
        time.sleep(5)  # Tunggu sebelum mencoba ulang
