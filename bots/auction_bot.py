from core.auction import generate_auction_brief
from telegram_sender import send_telegram_message
import os

BOT_TOKEN = os.getenv("TG_TOKEN_AUCTION")
CHAT_ID = os.getenv("TG_ID_AUCTION")

def run_auction_bot():
    auction_brief = generate_auction_brief()
    message = f"📅 오늘 서울 경매 브리핑\n━━━━━━━━━━━━━━━━━━\n{auction_brief}"
    send_telegram_message(BOT_TOKEN, CHAT_ID, message)

if __name__ == "__main__":
    run_auction_bot()
