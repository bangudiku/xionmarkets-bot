import asyncio
import json
import random
import datetime
from playwright.async_api import async_playwright
from colorama import Fore, Style

# Konfigurasi
MARKET_URL = "https://testnet.xionmarkets.com/market/xion1x89jut7kersq6nws063v2wdnl5l468j0vrpzxh0d7ezv0f9yn4qshyatss/1"
DELAY_AFTER_SUCCESS = 5
MAX_RETRIES = 3  # Jika gagal 3x, restart browser

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def run_market():
    while True:  # Loop utama agar tidak berhenti
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(
                        headless=True, 
                        args=["--disable-gpu", "--no-sandbox"]
                    )
                    context = await browser.new_context()

                    # Load Local Storage lebih aman
                    with open("config.json", "r") as f:
                        local_storage_data = json.load(f)

                    local_storage_script = f"""
                    for (let key in {json.dumps(local_storage_data)}) {{
                        localStorage.setItem(key, {json.dumps(local_storage_data)}[key]);
                    }}
                    """
                    await context.add_init_script(local_storage_script)

                    page = await context.new_page()

                    print(Fore.GREEN + f"{timestamp()} Memulai..." + Style.RESET_ALL)

                    # Buka Market
                    await page.goto(MARKET_URL)
                    await page.wait_for_selector("#trade", timeout=15000)
                    print(Fore.CYAN + f"{timestamp()} Halaman market siap!" + Style.RESET_ALL)

                    # Loop Auto Sell
                    while True:
                        try:
                            await page.wait_for_selector('button.amm-sell.mx-2', timeout=60000)
                            await page.click('button.amm-sell.mx-2')
                            await asyncio.sleep(2)

                            await page.wait_for_selector('button.outcomes.no.ms-1', timeout=60000)
                            await page.click('button.outcomes.no.ms-1')
                            await asyncio.sleep(2)

                            balance_text = await page.inner_text('span.usdc-balance')
                            balance = float(balance_text.replace(' share(s)', '').replace(',', ''))
                            print(Fore.YELLOW + f"{timestamp()} Saldo: {balance} USDC" + Style.RESET_ALL)

                            if balance < 1:
                                print(Fore.RED + f"{timestamp()} Saldo kurang! Tunggu 30 detik..." + Style.RESET_ALL)
                                await asyncio.sleep(30)
                                continue

                            sell_amount = random.choice([0.1, 0.2])
                            print(Fore.BLUE + f"{timestamp()} Menjual {sell_amount} share(s)..." + Style.RESET_ALL)

                            await page.fill('input#sell-input', str(sell_amount))
                            await page.click('button.trade-button')
                            await asyncio.sleep(2)

                            await page.click('button.trade-button')
                            await asyncio.sleep(2)

                            print(Fore.GREEN + f"{timestamp()} Order sukses! Tunggu {DELAY_AFTER_SUCCESS} detik..." + Style.RESET_ALL)
                            await asyncio.sleep(DELAY_AFTER_SUCCESS)

                        except Exception as e:
                            print(Fore.RED + f"{timestamp()} ERROR di transaksi: {e}" + Style.RESET_ALL)
                            print(Fore.CYAN + f"{timestamp()} Reloading halaman..." + Style.RESET_ALL)
                            await page.reload()
                            await asyncio.sleep(5)

            except Exception as e:
                print(Fore.RED + f"{timestamp()} ERROR BESAR: {e}" + Style.RESET_ALL)
                retry_count += 1
                print(Fore.YELLOW + f"{timestamp()} Restart Browser (Percobaan {retry_count}/{MAX_RETRIES})..." + Style.RESET_ALL)
                await asyncio.sleep(10)

        print(Fore.RED + f"{timestamp()} Gagal {MAX_RETRIES}x, restart total program..." + Style.RESET_ALL)
        await asyncio.sleep(10)  # Tunggu sebentar sebelum restart

# Jalankan Program
asyncio.run(run_market())
