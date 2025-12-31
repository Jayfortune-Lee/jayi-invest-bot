from telegram import Bot

def send_telegram_message(message: str, token: str, chat_id: str):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
