import sys
import os

# 루트 기준 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.macro import get_macro_message
from core.portfolio import get_portfolio_message
from telegram_sender import send_telegram_message

def run_market_bot():
    macro_msg = get_macro_message()
    portfolio_msg = get_portfolio_message()
    full_msg = f"{macro_msg}\n\n{portfolio_msg}"
    
    send_telegram_message(
        message=full_msg,
        token=os.environ["TG_TOKEN_MARKET"],
        chat_id=os.environ["TG_ID_MARKET"]
    )

if __name__ == "__main__":
    run_market_bot()
