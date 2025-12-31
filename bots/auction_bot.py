import sys
import os

# 루트 기준 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.auction import get_auction_message
from telegram_sender import send_telegram_message

def run_auction_bot():
    msg = get_auction_message()
    send_telegram_message(
        message=msg,
        token=os.environ["TG_TOKEN_AUCTION"],
        chat_id=os.environ["TG_ID_AUCTION"]
    )

if __name__ == "__main__":
    run_auction_bot()
