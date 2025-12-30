import requests

BOT_TOKEN = "8245058275:AAElfnU-WLlGodhWmjAmtJF4b9Dz39D_RQE"
CHAT_ID = "1537921863"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
response = requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": "✅ Telegram Desktop test message"
})

print(response.status_code)
print(response.text)
