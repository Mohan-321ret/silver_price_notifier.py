# silver_price_notifier.py
# AuraGold Silver Price Notifier (Local PC)

This project monitors the **live silver price from the AuraGold website** and sends **BUY / SELL desktop notifications** on your PC based on predefined threshold values.

It is designed to run **locally on a computer (Windows/Linux)** while the Python script is running.

---

## 📌 Features

- Fetches **live silver price** from https://auragold.in  
- Uses **Selenium** to handle JavaScript-rendered prices  
- Sends **desktop notifications** using Plyer  
- Alerts:
  - 📉 **BUY NOW** when price goes below buy threshold  
  - 📈 **SELL NOW** when price goes above sell threshold  
- Simple and beginner-friendly  

---

## 🧰 Technologies Used

- Python 3.x  
- Selenium  
- Chrome / Chromium Browser  
- Plyer (for desktop notifications)  

---

## 📦 Required Libraries

Install all dependencies using:

```bash
pip install -r requirements.txt


python aura_gold.py


