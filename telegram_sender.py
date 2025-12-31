import requests

def send_telegram_message(message: str, token: str, chat_id: str):
    """
    Telegram 메시지 발송
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        print(f"⚠️ Telegram 발송 실패: {response.text}")
    return response.ok
