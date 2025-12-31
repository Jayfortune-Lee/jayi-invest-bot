import os
from core.auction import get_auction_brief
from core.telegram_sender import send_telegram_message

def run_auction_bot():
    message = get_auction_brief()
    chat_id = os.environ.get("TG_ID_AUCTION")
    send_telegram_message(chat_id, message)

if __name__ == "__main__":
    run_auction_bot()
