# XionMarkets Bot (Testnet)

## 🚀 Overview
Bot otomatis untuk trading di **XionMarkets Testnet** menggunakan **Playwright**.

## 📌 Features
- **Market Selection**: Pilih market yang ingin digunakan.
- **Buy/Sell Automation**: Bisa memilih transaksi **BUY** atau **SELL**.
- **YES/NO Selection**: Memilih outcome **YES** atau **NO**.
- **Balance Checking**: Mengecek saldo sebelum transaksi.
- **Randomized Order Amount**: Bisa menginput jumlah manual atau memilih **random 1-30**.
- **Auto Retry on Insufficient Funds**: Jika saldo tidak cukup, bot akan menunggu dan mencoba lagi.

---

## 📦 Installation & Setup

### 1️⃣ **Clone Repository**
Buka terminal atau CMD, lalu jalankan perintah berikut:
```sh
git clone https://github.com/bangudiku/xionmarkets-bot.git
cd xionmarkets-bot
```

### 2️⃣ **Install Dependencies**
Pastikan **Python** sudah terinstal. Jika belum, unduh dari [python.org](https://www.python.org/downloads/). Lalu jalankan perintah berikut:
```sh
pip install -r requirements.txt
pip install playwright
python -m playwright install
```

### 3️⃣ **Configure Your Account**
Edit file `config.json` dengan data akun Anda:

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

#### **Cara Mendapatkan Data Local Storage**
1. Buka [XionMarkets Testnet](https://testnet.xionmarkets.com) di Google Chrome.
2. Tekan `F12` untuk membuka **Developer Tools**.
3. Pergi ke tab **Console** dan masukkan perintah berikut:
   ```js
   console.log(JSON.stringify(localStorage, null, 2));
   ```
4. Salin hasilnya dan tempelkan ke dalam `config.json`.

---

## 🔄 Running the Bot
Setelah konfigurasi selesai, jalankan bot dengan perintah berikut:
```sh
python bot.py
```
Bot akan otomatis:
1. Login ke XionMarkets.
2. Membuka halaman market.
3. Memilih outcome YES/NO.
4. Mengecek saldo sebelum transaksi.
5. Melakukan transaksi sesuai pilihan BUY/SELL.
6. Mengulang proses setelah transaksi selesai.

---

## 🔄 Updating the Code
Jika ada update script, jalankan perintah:
```sh
git pull origin main
```
Jika ingin mengedit dan menyimpan perubahan:
```sh
git add .
git commit -m "Update fitur X"
git push origin main
```

---

## ❓ Troubleshooting
Jika terjadi error, coba langkah berikut:
- Pastikan **Google Chrome** dan **ChromeDriver** sudah terinstal.
- Periksa kembali apakah `config.json` sudah diisi dengan benar.
- Jika ada masalah dengan Python 2, coba jalankan dengan `python3 bot.py`.

Jika masih mengalami masalah, buka **Issue** di GitHub! 🎯

---

## 📜 License
Bot ini bersifat open-source dan dapat digunakan oleh siapa saja.

**DWYOR!!! THIS IS FOR EDUCATION ONLY**

- Buy Coffee SOL: `fXTzeQ9xm4nENv5gR4V5LcCMHQnexrcqnCoye1Jb6tV`
- [Telegram](https://t.me/dwiputraofficial)

