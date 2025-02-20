import json
import asyncio
import datetime
from playwright.async_api import async_playwright
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# 🔧 Konfigurasi
MARKET_URL = "https://testnet.xionmarkets.com/market/xion1x89jut7kersq6nws063v2wdnl5l468j0vrpzxh0d7ezv0f9yn4qshyatss/1"
DELAY_AFTER_SUCCESS = 5  # Tunggu sebentar setelah transaksi sebelum cek saldo lagi


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def main():
    while True:  # Loop utama agar tidak berhenti
        async with async_playwright() as p:
            # Buka Browser dalam mode headless
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # Coba buka halaman utama dengan mekanisme retry
            while True:
                try:
                    await page.goto("https://testnet.xionmarkets.com", timeout=30000)
                    await page.wait_for_selector("body", timeout=10000)
                    print(Fore.GREEN + f"{timestamp()} Halaman utama berhasil dimuat!")
                    break  # Keluar dari loop jika sukses
                except Exception as e:
                    print(Fore.RED + f"{timestamp()} Gagal membuka halaman utama: {e}")
                    print(Fore.CYAN + f"{timestamp()} Mencoba kembali dalam 5 detik...")
                    await asyncio.sleep(5)

            # Muatan Local Storage untuk Login
            with open("config.json", "r") as f:
                local_storage_data = json.load(f)

            for key, value in local_storage_data.items():
                await page.evaluate(f"window.localStorage.setItem('{key}', '{value}');")

            print(Fore.CYAN + f"{timestamp()} Local Storage berhasil dimasukkan! Akun masuk otomatis!")
            await page.reload()

            # Coba buka halaman Market dengan retry jika error
            while True:
                try:
                    await page.goto(MARKET_URL, timeout=30000)
                    await page.wait_for_selector(".trade-button", timeout=15000)
                    print(Fore.GREEN + f"{timestamp()} Halaman market berhasil dimuat!")
                    break  # Keluar dari loop jika sukses
                except Exception as e:
                    print(Fore.RED + f"{timestamp()} Gagal membuka halaman market: {e}")
                    print(Fore.CYAN + f"{timestamp()} Mencoba kembali dalam 5 detik...")
                    await asyncio.sleep(5)

            await asyncio.sleep(20)

            # Loop Auto Buy
            while True:
                try:
                    # Cek Saldo
                    balance_text = await page.inner_text('xpath=//*[@id="trade"]/div[3]/div/span[2]')
                    balance = float(balance_text.replace(',', ''))
                    print(Fore.YELLOW + f"{timestamp()} Saldo saat ini: {balance} USDC")

                    if balance < 1:
                        print(Fore.RED + f"{timestamp()} Saldo tidak cukup! Menunggu 30 detik sebelum mencoba lagi...")
                        await asyncio.sleep(30)
                        continue

                    # Proses Pembelian (ubah langkah ini jika ada perubahan kebutuhan)
                    await page.click('button.outcomes.no.ms-1')
                    await asyncio.sleep(2)

                    # Masukkan Jumlah Pembelian
                    await page.click('xpath=//*[@id="buy-input"]')
                    await page.fill('xpath=//*[@id="buy-input"]', "0.2")

                    # Klik Tombol Buy
                    await page.click(".trade-button")
                    await asyncio.sleep(2)

                    # Konfirmasi Transaksi
                    await page.click('xpath=//*[@id="root"]/main/div[1]/div/div[2]/div[3]/button')
                    await asyncio.sleep(2)

                    # Tutup Pop-up jika ada
                    try:
                        await page.click('xpath=//*[@id="root"]/main/div[1]/div/div[1]/div[2]/img', timeout=5000)
                        print(Fore.GREEN + f"{timestamp()} Pop-up tertutup!")
                    except:
                        print(Fore.CYAN + f"{timestamp()} Tidak ada pop-up, lanjutkan proses...")

                    print(Fore.GREEN + f"{timestamp()} Order berhasil! Menunggu {DELAY_AFTER_SUCCESS} detik sebelum cek saldo lagi...")
                    await asyncio.sleep(DELAY_AFTER_SUCCESS)

                except Exception as e:
                    print(Fore.RED + f"{timestamp()} Error dalam loop utama: {e}")
                    print(Fore.CYAN + f"{timestamp()} Reloading halaman...")
                    await page.reload()
                    await asyncio.sleep(5)

            await browser.close()


# Jalankan Kode
asyncio.run(main())
