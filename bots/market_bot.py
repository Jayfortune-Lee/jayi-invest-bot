import os
from core.macro import auto_as_macro_prompt
from core.portfolio import get_portfolio_message
from telegram_sender import send_telegram_message

def run_market_bot():
    as_briefing = auto_as_macro_prompt()
    portfolio_msg = get_portfolio_message()
    final_message = f"📅 오늘의 전략 브리핑\n━━━━━━━━━━━━━━━━━━\n{as_briefing}\n━━━━━━━━━━━━━━━━━━\n{portfolio_msg}\n━━━━━━━━━━━━━━━━━━"

    send_telegram_message(
        final_message,
        token=os.environ["TG_TOKEN_MARKET"],
        chat_id=os.environ["TG_ID"]
    )

if __name__ == "__main__":
    run_market_bot()
