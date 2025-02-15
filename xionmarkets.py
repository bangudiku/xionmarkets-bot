import json
import asyncio
from playwright.async_api import async_playwright

# 🔧 **Konfigurasi**
MARKET_URL = "https://testnet.xionmarkets.com/market/xion1x89jut7kersq6nws063v2wdnl5l468j0vrpzxh0d7ezv0f9yn4qshyatss/1"
DELAY_AFTER_SUCCESS = 5  # Tunggu sebentar setelah transaksi sebelum cek saldo lagi

async def main():
    async with async_playwright() as p:
        # 🌐 **Buka Browser**
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 🔗 **Buka XionMarkets**
        await page.goto("https://testnet.xionmarkets.com")
        await page.wait_for_selector("body", timeout=10000)
        print("✅ Halaman utama berhasil dimuat!")

        # 🔑 **Muatan Local Storage untuk Login**
        with open("config.json", "r") as f:
            local_storage_data = json.load(f)

        for key, value in local_storage_data.items():
            await page.evaluate(f"window.localStorage.setItem('{key}', '{value}');")

        print("✅ Local Storage berhasil dimasukkan!")
        await page.reload()
        
        # 🏪 **Masuk ke Halaman Market**
        await page.goto(MARKET_URL)
        await page.wait_for_selector("#trade", timeout=15000)
        print("✅ Halaman market berhasil dimuat!")

        # 🔄 **Loop Auto Buy**
        while True:
            try:
                # 🏦 **Ambil Saldo**
                balance_text = await page.inner_text('xpath=//*[@id="trade"]/div[3]/div/span[2]')
                balance = float(balance_text.replace(',', ''))
                print(f"💰 Saldo saat ini: {balance} USDC")

                if balance < 1:
                    print("❌ Saldo tidak cukup! Tunggu 30 detik...")
                    await asyncio.sleep(30)
                    continue

                # 📥 **Masukkan Jumlah Pembelian**
                await page.click('xpath=//*[@id="buy-input"]')
                await page.fill('xpath=//*[@id="buy-input"]', "1")

                # 🛒 **Klik Buy**
                await page.click('xpath=//*[@id="trade"]/div[6]/button')
                await asyncio.sleep(2)

                # ✅ **Konfirmasi Transaksi**
                await page.click('xpath=//*[@id="root"]/main/div[1]/div/div[2]/div[3]/button')
                await asyncio.sleep(2)

                # ❌ **Tutup Pop-up jika ada**
                try:
                    await page.click('xpath=//*[@id="root"]/main/div[1]/div/div[1]/div[2]/img', timeout=5000)
                    print("✅ Pop-up tertutup!")
                except:
                    print("ℹ️ Tidak ada pop-up, lanjutkan proses...")

                # ⏳ **Skip Menunggu Konfirmasi, Langsung Cek Saldo Lagi**
                print(f"✅ Order berhasil dieksekusi! Tunggu {DELAY_AFTER_SUCCESS} detik sebelum cek saldo lagi...")
                await asyncio.sleep(DELAY_AFTER_SUCCESS)

            except Exception as e:
                print(f"❌ Error dalam loop utama: {e}")
                await asyncio.sleep(5)

        # ❌ **Tutup Browser**
        await browser.close()

# 🚀 **Jalankan Kode**
asyncio.run(main())
