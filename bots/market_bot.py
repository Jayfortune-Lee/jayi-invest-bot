import sys
import os

# 루트 경로를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.macro import get_macro_message
from core.portfolio import get_portfolio_message
from telegram_sender import send_telegram_message

def run_market_bot():
    macro_msg = get_macro_message()            # 글로벌 자동차/AS + 정책/거시 뉴스
    portfolio_msg = get_portfolio_message()    # 주식 포트폴리오 전략
    full_msg = f"{macro_msg}\n\n{portfolio_msg}"
    
    send_telegram_message(
        message=full_msg,
        token=os.environ["TG_TOKEN_MARKET"],
        chat_id=os.environ["TG_ID_MARKET"]
    )

if __name__ == "__main__":
    run_market_bot()
