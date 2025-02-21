import json
import asyncio
import random
from playwright.async_api import async_playwright
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Daftar Market
MARKETS = {
    "Will Trump": "https://testnet.xionmarkets.com/market/xion1yu754737075cdw2qj075w27c7eh30qg4w6ewl7synyguzhuutntqzj3vgl/3",
    "Will China invade Taiwan in 2025": "https://testnet.xionmarkets.com/market/xion1pu77egm5hjn9tzydk9a0cnl74zr0m08q8j7vnwmdx079qj5n6xtqe9ljex/2",
    "Will MrBeast buy TikTok": "https://testnet.xionmarkets.com/market/xion1x89jut7kersq6nws063v2wdnl5l468j0vrpzxh0d7ezv0f9yn4qshyatss/1"
}

DELAY_AFTER_SUCCESS = 5  # Waktu tunggu setelah transaksi berhasil

async def main():
    print(Fore.CYAN + "🔹 Pilih Market yang ingin digunakan:")
    market_list = list(MARKETS.keys())  
    for idx, market_name in enumerate(market_list, start=1):
        print(f"{Fore.YELLOW}{idx}. {market_name}")

    # Pilihan market
    while True:
        try:
            choice = int(input(Fore.CYAN + "Masukkan nomor market: ")) - 1
            if 0 <= choice < len(market_list):
                selected_market_name = market_list[choice]
                selected_market_url = MARKETS[selected_market_name]
                print(Fore.GREEN + f"✅ Market '{selected_market_name}' dipilih!\n")
                break
            else:
                print(Fore.RED + "❌ Pilihan tidak valid! Coba lagi.")
        except ValueError:
            print(Fore.RED + "❌ Masukkan angka yang benar!")

    # Pilihan transaksi (Buy/Sell)
    while True:
        print(Fore.CYAN + "\n🔹 Pilih jenis transaksi:")
        print(Fore.YELLOW + "1. Buy")
        print(Fore.YELLOW + "2. Sell")
        
        transaction_choice = input(Fore.CYAN + "Masukkan nomor pilihan: ").strip()
        if transaction_choice == "1":
            transaction_type = "buy"
            break
        elif transaction_choice == "2":
            transaction_type = "sell"
            break
        else:
            print(Fore.RED + "❌ Pilihan tidak valid! Masukkan 1 atau 2.")

    # Pilihan YES/NO hanya sekali di awal
    while True:
        print(Fore.CYAN + "\n🔹 Pilih hasil transaksi:")
        print(Fore.YELLOW + "1. YES")
        print(Fore.YELLOW + "2. NO")

        outcome_choice = input(Fore.CYAN + "Masukkan nomor pilihan: ").strip()
        if outcome_choice == "1":
            outcome_selector = "button.outcomes.yes.me-1"
            outcome_text = "YES"
            break
        elif outcome_choice == "2":
            outcome_selector = "button.outcomes.no.ms-1"
            outcome_text = "NO"
            break
        else:
            print(Fore.RED + "❌ Pilihan tidak valid! Masukkan 1 atau 2.")

    # Input jumlah dengan validasi angka (integer/float)
    while True:
        amount_input = input(Fore.CYAN + "Masukkan jumlah (atau ketik 'random' untuk nilai acak 1-30): ").strip()

        if amount_input.lower() == "random":
            amount = round(random.uniform(1, 30), 2)  # Gunakan float acak dengan 2 desimal
            print(Fore.YELLOW + f"🎲 Random amount dipilih: {amount}")
            break

        try:
            amount = float(amount_input)  # Bisa menerima bilangan desimal
            if amount <= 0:
                print(Fore.RED + "❌ Jumlah harus lebih dari 0!")
            else:
                break
        except ValueError:
            print(Fore.RED + "❌ Input jumlah tidak valid! Masukkan angka.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://testnet.xionmarkets.com")
        await page.wait_for_selector("body", timeout=10000)
        print(Fore.GREEN + "✅ Halaman utama berhasil dimuat!")

        # Load Local Storage
        with open("config.json", "r") as f:
            local_storage_data = json.load(f)

        for key, value in local_storage_data.items():
            await page.evaluate(f"window.localStorage.setItem('{key}', '{value}');")

        print(Fore.GREEN + "✅ Local Storage berhasil dimasukkan!")
        await page.reload()

        # Akses market
        await page.goto(selected_market_url)
        await page.wait_for_selector("#trade", timeout=15000)
        print(Fore.GREEN + f"✅ Halaman market '{selected_market_name}' berhasil dimuat!")

        # Pilih YES/NO hanya sekali di awal
        await page.wait_for_selector(outcome_selector, timeout=60000)
        await page.click(outcome_selector)
        print(Fore.YELLOW + f"🟡 Memilih {outcome_text}...")

        while True:
            try:
                action_selector = "button.amm-buy.mx-2" if transaction_type == "buy" else "button.amm-sell.mx-2"
                await page.wait_for_selector(action_selector, timeout=60000)
                await page.click(action_selector)
                await asyncio.sleep(2)

                # Cek saldo berdasarkan transaksi
                if transaction_type == "buy":
                    balance_text = await page.inner_text("span.usdc-balance:last-child")
                    unit = "USDC"
                else:
                    balance_text = await page.inner_text("span.share-balance:last-child")
                    unit = "share(s)"

                balance = float(balance_text.replace(",", "").strip())  
                print(Fore.GREEN + f"💰 Saldo saat ini: {balance} {unit}")

                if balance < amount:
                    print(Fore.RED + "❌ Saldo tidak cukup! Tunggu 30 detik...") 
                    await asyncio.sleep(30)
                    continue

                input_selector = "input#buy-input" if transaction_type == "buy" else "input#sell-input"
                await page.fill(input_selector, str(amount))  
                print(Fore.BLUE + f"📥 Melakukan {transaction_type} {amount} share(s)...")

                await page.click("button[type='submit'].trade-button")  
                await asyncio.sleep(2)

                await page.click("button[type='button'].trade-button")  
                await asyncio.sleep(2)

                print(Fore.GREEN + f"✅ {transaction_type.capitalize()} berhasil di '{selected_market_name}'!")
                await asyncio.sleep(DELAY_AFTER_SUCCESS)

            except Exception as e:
                print(Fore.RED + f"❌ Error dalam loop utama: {e}")
                await asyncio.sleep(5)

        await browser.close()

asyncio.run(main())
