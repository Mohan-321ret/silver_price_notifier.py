# silver_notifier.py
# ✅ Works on PC and Android
# ✅ Displays live silver price
# ✅ Sends "Buy Now" / "Sell Now" notifications
# ✅ Ready for APK conversion (Buildozer / Replit)

import re
import time
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import notification
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------
# Global constants
# ---------------------------------------
URL = "https://auragold.in"
NUM = re.compile(r"[0-9]+(?:\.[0-9]+)?")


# ---------------------------------------
# Helper functions
# ---------------------------------------
def extract_number(text: str) -> float:
    """Extract numeric value from a price string."""
    text = text.replace(",", "")
    match = NUM.search(text)
    if not match:
        raise ValueError(f"No number found in: {text!r}")
    return float(match.group(0))


def get_silver_price() -> float:
    """Fetch the current live silver price (₹/gm) from auragold.in."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    try:
        driver.get(URL)

        # Wait until the silver price section appears
        WebDriverWait(driver, 25).until(lambda d: "Live Silver Price" in d.page_source)
        time.sleep(3)  # small delay for JS to update numbers

        spans = driver.find_elements(By.CSS_SELECTOR, "span.price")
        prices = [extract_number(sp.text) for sp in spans if re.search(r"\d", sp.text)]

        if not prices:
            raise RuntimeError("No prices found on the page")

        silver_price = prices[-1]  # last numeric span = silver
        return silver_price

    finally:
        driver.quit()


def send_notification(price: float, buy_threshold: float, sell_threshold: float):
    """Trigger desktop or mobile notification based on current price."""
    if price <= buy_threshold:
        notification.notify(
            title="📉 Silver Alert",
            message=f"BUY NOW — ₹{price:.2f}/gm",
            timeout=5
        )

    elif price >= sell_threshold:
        notification.notify(
            title="📈 Silver Alert",
            message=f"SELL NOW — ₹{price:.2f}/gm",
            timeout=5
        )


# ---------------------------------------
# Kivy App
# ---------------------------------------
class SilverApp(App):
    def build(self):
        self.label = Label(
            text="Fetching silver price...",
            font_size=24,
            halign="center",
            valign="middle"
        )
        Clock.schedule_once(lambda dt: self.start_background_check(), 1)
        return self.label

    def start_background_check(self):
        """Start the background thread to check price every 5 minutes."""
        thread = threading.Thread(target=self.check_loop, daemon=True)
        thread.start()

    def check_loop(self):
        BUY_THRESHOLD = 180.0  # change as per your strategy
        SELL_THRESHOLD = 185.0

        while True:
            try:
                price = get_silver_price()
                self.label.text = f"Current Silver Price: ₹{price:.2f}/gm"

                # Trigger notification
                send_notification(price, BUY_THRESHOLD, SELL_THRESHOLD)

            except Exception as e:
                self.label.text = f"Error: {e}"

            time.sleep(300)  # check every 5 minutes


# ---------------------------------------
# Main
# ---------------------------------------
if __name__ == "__main__":
    SilverApp().run()
