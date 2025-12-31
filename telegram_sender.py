import os
import requests

TG_TOKEN = os.getenv("TG_TOKEN")
TG_ID = os.getenv("TG_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.json()
