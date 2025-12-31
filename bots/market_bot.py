import os
from core.macro import auto_as_macro_prompt
from core.portfolio import auto_portfolio_brief
from telegram_sender import send_telegram_message

def run_market_bot():
    macro_msg = auto_as_macro_prompt()      # 글로벌 자동차/AS 분석
    portfolio_msg = auto_portfolio_brief() # 주식 포트폴리오 전략
    full_msg = f"{macro_msg}\n\n{portfolio_msg}"
    
    send_telegram_message(
        full_msg,
        token=os.environ["TG_TOKEN_MARKET"],
        chat_id=os.environ["TG_ID_MARKET"]
    )

if __name__ == "__main__":
    run_market_bot()
