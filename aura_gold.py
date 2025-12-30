# aura_gold.py
# AuraGold Silver BUY / SELL Notifier (Telegram)
# Runs locally on PC using Selenium

import re
import time
import threading
import requests

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
URL = "https://auragold.in"

BUY_THRESHOLD = 180.0
SELL_THRESHOLD = 185.0

BOT_TOKEN = "8245058275:AAElfnU-WLlGodhWmjAmtJF4b9Dz39D_RQE"
CHAT_ID = "1537921863"

NUM = re.compile(r"[0-9]+(?:\.[0-9]+)?")

last_signal = None  # prevents repeated alerts

# --------------------------------------------------
# TELEGRAM
# --------------------------------------------------
def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

# --------------------------------------------------
# PRICE EXTRACTION
# --------------------------------------------------
def extract_number(text: str) -> float:
    text = text.replace(",", "")
    match = NUM.search(text)
    if not match:
        raise ValueError(f"No number found in: {text}")
    return float(match.group(0))

def get_silver_price() -> float:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )

    try:
        driver.get(URL)
        WebDriverWait(driver, 25).until(
            lambda d: "Live Silver Price" in d.page_source
        )
        time.sleep(3)

        spans = driver.find_elements(By.CSS_SELECTOR, "span.price")
        prices = [
            extract_number(sp.text)
            for sp in spans
            if re.search(r"\d", sp.text)
        ]

        if not prices:
            raise RuntimeError("Silver price not found")

        return prices[-1]  # last number = silver

    finally:
        driver.quit()

# --------------------------------------------------
# ALERT LOGIC
# --------------------------------------------------
def check_and_notify(price: float):
    global last_signal

    if price <= BUY_THRESHOLD and last_signal != "BUY":
        send_telegram(f"📉 BUY NOW\nSilver Price: ₹{price:.2f}/gm")
        last_signal = "BUY"

    elif price >= SELL_THRESHOLD and last_signal != "SELL":
        send_telegram(f"📈 SELL NOW\nSilver Price: ₹{price:.2f}/gm")
        last_signal = "SELL"

# --------------------------------------------------
# KIVY APP (STATUS DISPLAY)
# --------------------------------------------------
class SilverApp(App):
    def build(self):
        self.label = Label(
            text="Fetching silver price...",
            font_size=22,
            halign="center",
            valign="middle"
        )
        Clock.schedule_once(lambda dt: self.start_worker(), 1)
        return self.label

    def start_worker(self):
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while True:
            try:
                price = get_silver_price()
                self.label.text = f"Current Silver Price: ₹{price:.2f}/gm"
                check_and_notify(price)

            except Exception as e:
                self.label.text = f"Error: {e}"

            time.sleep(300)  # 5 minutes

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    SilverApp().run()
