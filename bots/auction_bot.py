# Auction Jayi Bot (서울 아파트 경매)
import os
from core.auction import get_auction_message
from telegram_sender import send_telegram_message

def run_auction_bot():
    auction_msg = get_auction_message()
    send_telegram_message(
        auction_msg,
        token=os.environ["TG_TOKEN_AUCTION"],
        chat_id=os.environ["TG_ID"]
    )

if __name__ == "__main__":
    run_auction_bot()
