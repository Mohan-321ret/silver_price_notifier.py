# test.py
import requests

BOT_TOKEN = "8580016419:AAEILwqqaBEPLTKChITlJ1411_EU2LRgl90"
CHAT_ID = "1537921863"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })
    r.raise_for_status()

if __name__ == "__main__":
    send_telegram("✅ Telegram test successful!\nYou will receive BUY/SELL alerts here.")
