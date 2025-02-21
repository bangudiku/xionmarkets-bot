import json
import asyncio
import random
from playwright.async_api import async_playwright

MARKETS = {
    "Will Trump": "https://testnet.xionmarkets.com/market/xion1yu754737075cdw2qj075w27c7eh30qg4w6ewl7synyguzhuutntqzj3vgl/3",
    "Will China invade Taiwan in 2025": "https://testnet.xionmarkets.com/market/xion1pu77egm5hjn9tzydk9a0cnl74zr0m08q8j7vnwmdx079qj5n6xtqe9ljex/2",
    "Will MrBeast buy TikTok": "https://testnet.xionmarkets.com/market/xion1x89jut7kersq6nws063v2wdnl5l468j0vrpzxh0d7ezv0f9yn4qshyatss/1"
}

DELAY_AFTER_SUCCESS = 5  

async def main():
    print("🔹 Pilih Market yang ingin digunakan:")
    market_list = list(MARKETS.keys())  
    for idx, market_name in enumerate(market_list, start=1):
        print(f"{idx}. {market_name}")

    while True:
        try:
            choice = int(input("Masukkan nomor market: ")) - 1
            if 0 <= choice < len(market_list):
                selected_market_name = market_list[choice]
                selected_market_url = MARKETS[selected_market_name]
                print(f"✅ Market '{selected_market_name}' dipilih!\n")
                break
            else:
                print("❌ Pilihan tidak valid! Coba lagi.")
        except ValueError:
            print("❌ Masukkan angka yang benar!")

    while True:
        transaction_type = input("Pilih transaksi (buy/sell): ").strip().lower()
        if transaction_type in ["buy", "sell"]:
            break
        print("❌ Pilihan harus 'buy' atau 'sell'!")

    amount_input = input("Masukkan jumlah (atau ketik 'random' untuk nilai acak 1-30): ").strip()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://testnet.xionmarkets.com")
        await page.wait_for_selector("body", timeout=10000)
        print("✅ Halaman utama berhasil dimuat!")

        with open("config.json", "r") as f:
            local_storage_data = json.load(f)

        for key, value in local_storage_data.items():
            await page.evaluate(f"window.localStorage.setItem('{key}', '{value}');")

        print("✅ Local Storage berhasil dimasukkan!")
        await page.reload()
        
        await page.goto(selected_market_url)
        await page.wait_for_selector("#trade", timeout=15000)
        print(f"✅ Halaman market '{selected_market_name}' berhasil dimuat!")

        while True:
            try:
                action_selector = "button.amm-buy.mx-2" if transaction_type == "buy" else "button.amm-sell.mx-2"
                await page.wait_for_selector(action_selector, timeout=60000)
                await page.click(action_selector)
                await asyncio.sleep(2)

                await page.wait_for_selector("button.outcomes.no.ms-1", timeout=60000)
                await page.click("button.outcomes.no.ms-1")  
                await asyncio.sleep(2)

                # 🆕 **Ambil balance berdasarkan jenis transaksi**
                if transaction_type == "buy":
                    balance_text = await page.inner_text("div.d-flex.align-items-center.justify-content-end > span.usdc-balance:last-child")
                    balance = float(balance_text.replace(",", "").strip())  # 🔹 USDC Balance
                    print(f"💰 Saldo saat ini: {balance} USDC")
                else:  # Sell
                    balance_text = await page.inner_text('span.usdc-balance')  # 🔹 Share Balance
                    balance = float(balance_text.replace(' share(s)', '').replace(',', ''))
                    print(f"💰 Saldo saat ini: {balance} share(s)")

                if balance < 1:
                    print("❌ Saldo tidak cukup! Tunggu 30 detik...") 
                    await asyncio.sleep(30)
                    continue

                # 🆕 **Pastikan `amount` di-random setiap loop**
                if amount_input.lower() == "random":
                    amount = random.randint(1, 30)  # 🔄 Generate angka baru setiap loop
                else:
                    amount = int(amount_input)

                input_selector = "input#buy-input" if transaction_type == "buy" else "input#sell-input"
                await page.fill(input_selector, str(amount))  
                print(f"📥 Melakukan {transaction_type} {amount} share(s)...")

                await page.click("button[type='submit'].trade-button")  
                await asyncio.sleep(2)

                await page.click("button[type='button'].trade-button")  
                await asyncio.sleep(2)

                print(f"✅ {transaction_type.capitalize()} berhasil di '{selected_market_name}'! Tunggu {DELAY_AFTER_SUCCESS} detik sebelum cek saldo lagi...")
                await asyncio.sleep(DELAY_AFTER_SUCCESS)

            except Exception as e:
                print(f"❌ Error dalam loop utama: {e}")
                await asyncio.sleep(5)

        await browser.close()

asyncio.run(main())
