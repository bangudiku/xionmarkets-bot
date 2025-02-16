# XionMarkets Bot (Testnet) ALAKADARNYA!

## MAKE SURE YOUR INTERNET IS GOOD!

Bot otomatis untuk trading di XionMarkets Testnet menggunakan Selenium.

## 📌 Features
- **Automatic Login**: Uses local storage data.
- **Auto Buy**: Automatically purchases assets on XionMarkets.
- **Balance Checking**: Checks balance before making a purchase.
- **Auto Refresh**: If a transaction fails, the bot will automatically refresh and retry.

---

## 📦 Installation & Setup

### 1️⃣ **Clone the Repository**
Open a terminal or CMD and run the following commands:
```sh
git clone https://github.com/bangudiku/xionmarkets-bot.git
cd xionmarkets-bot
```
**Replace `USERNAME` with your GitHub username!**

### 2️⃣ **Install Dependencies**
Make sure you have **Python** installed. If not, download it from [python.org](https://www.python.org/downloads/). Then, run the following command:
```sh
pip install -r requirements.txt
python -m pip install -r requirements.txt

```

### 3️⃣ **Configure Your Account**
Edit the `config.json` file with your account data:

#### **Open `config.json` and fill it with your local storage data:**
```json
{
    "trust:cache:timestamp": "{\"timestamp\":1739383134806}",
    "xion-authz-granter-account": "YOUR_ACCOUNT_ADDRESS",
    "delay": "1739469473",
    "converted": "true",
    "ethereum-https://testnet.xionmarkets.com": "{\"chainId\":\"0x465\"}",
    "isWhitelist": "false",
    "loglevel": "SILENT",
    "xion-authz-temp-account": "YOUR_ENCRYPTED_WALLET_DATA",
    "binance-https://testnet.xionmarkets.com": "{}"
}
```

> **How to retrieve local storage data:**
> 1. Open [XionMarkets Testnet](https://testnet.xionmarkets.com) in Chrome.
> 2. Press `F12` to open **Developer Tools**.
  3. Go to the **Console** tab and enter the following command:
>    ```js
>    console.log(JSON.stringify(localStorage, null, 2));
>    ```
> 4. Copy the output and paste it into `config.json`.
---

## 🚀 Running the Bot
Once configured, run the bot using:
```sh
python xionmarkets.py
```
The bot will automatically:
1. Log in to XionMarkets.
2. Open the market page.
3. Check the balance.
4. Purchase assets automatically.
5. Wait for the transaction to complete and repeat the process.

---

## 🔄 Updating the Code
If there are updates to the script, run:
```sh
git pull origin main
```
If you want to edit and save changes:
```sh
git add .
git commit -m "Update feature X"
git push origin main
```

---

## ❓ Troubleshooting
If you encounter errors, try the following steps:
- Ensure **Google Chrome** and **ChromeDriver** are installed.
- Make sure `config.json` is filled in correctly.
- Try running with `python3 bot.py` if there are issues with Python 2.

If you still have issues, open an **Issue** on GitHub! 🎯

---

## 📜 License
This bot is open-source and available for anyone to use.

**DWYOR!!! THIS IS FOR EDUCATION ONLY** 
**Buy Coffee SOL fXTzeQ9xm4nENv5gR4V5LcCMHQnexrcqnCoye1Jb6tV** 

