import json
import asyncio
import random
from playwright.async_api import async_playwright

# 🔧 **Konfigurasi**
MARKET_URL = "https://testnet.xionmarkets.com/market/xion1x89jut7kersq6nws063v2wdnl5l468j0vrpzxh0d7ezv0f9yn4qshyatss/1"
DELAY_AFTER_SUCCESS = 5  # Tunggu sebentar setelah transaksi sebelum cek saldo lagi

async def main():
    async with async_playwright() as p:
        # 🌐 **Buka Browser dalam mode headless**
        browser = await p.chromium.launch(headless=True)
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
        
        # 🏩 **Masuk ke Halaman Market**
        await page.goto(MARKET_URL)
        await page.wait_for_selector("#trade", timeout=15000)
        print("✅ Halaman market berhasil dimuat!")

        # 🔄 **Loop Auto Sell**
        while True:
            try:
                # 🏩 **Klik Menu Sell**
                await page.wait_for_selector('button.amm-sell.mx-2', timeout=60000)  # Tunggu hingga tombol Sell muncul
                await page.click('button.amm-sell.mx-2')  # Klik tombol Menu Sell
                await asyncio.sleep(2)

                # 🛀 **Klik NO**
                await page.wait_for_selector('button.outcomes.no.ms-1', timeout=60000)  # Tunggu hingga tombol NO muncul
                await page.click('button.outcomes.no.ms-1')  # Pilih "No"
                await asyncio.sleep(2)

                # 🏦 **Ambil Saldo** setelah memilih NO
                balance_text = await page.inner_text('span.usdc-balance')  # Ambil saldo dari halaman
                balance = float(balance_text.replace(' share(s)', '').replace(',', ''))
                print(f"💰 Saldo saat ini: {balance} share(s)")

                if balance < 1:
                    print("❌ Saldo tidak cukup! Tunggu 30 detik...")
                    await asyncio.sleep(30)
                    continue

                # 📥 **Masukkan Jumlah Penjualan (1 atau 2)**
                sell_amount = random.choice([1, 2])  # Pilih angka secara acak (1 atau 2)
                await page.fill('input#sell-input', str(sell_amount))  # Isi input sell dengan jumlah yang dipilih
                print(f"📥 Menjual {sell_amount} share(s)...")

                # 🛒 **Klik Tombol Eksekusi Sell**
                await page.click('button.trade-button')  # Tombol Eksekusi Sell
                await asyncio.sleep(2)

                # ✅ **Klik Tombol Confirm Action**
                await page.click('button.trade-button')  # Tombol Confirm Action
                await asyncio.sleep(2)

                # ⏳ **Tunggu Konfirmasi Selesai**
                print(f"✅ Order berhasil dieksekusi! Tunggu {DELAY_AFTER_SUCCESS} detik sebelum cek saldo lagi...")
                await asyncio.sleep(DELAY_AFTER_SUCCESS)

            except Exception as e:
                print(f"❌ Error dalam loop utama: {e}")
                await asyncio.sleep(5)

        # ❌ **Tutup Browser**
        await browser.close()

# 🚀 **Jalankan Kode**
asyncio.run(main())
