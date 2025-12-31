import os
from core.macro import auto_as_macro_prompt
from core.portfolio import get_portfolio_message
from telegram_sender import send_telegram_message

def run_market_bot():
    # 글로벌 자동차/AS 시장 브리핑
    as_briefing = auto_as_macro_prompt()

    # 주식 포트폴리오 전략 메시지
    portfolio_msg = get_portfolio_message()

    # 최종 메시지 조합
    final_message = f"📅 오늘의 전략 브리핑\n━━━━━━━━━━━━━━━━━━\n"
    final_message += f"{as_briefing}\n━━━━━━━━━━━━━━━━━━\n"
    final_message += f"{portfolio_msg}\n━━━━━━━━━━━━━━━━━━"

    # Telegram 발송
    send_telegram_message(
        final_message,
        token=os.environ["TG_TOKEN_MARKET"],
        chat_id=os.environ["TG_ID"]
    )

if __name__ == "__main__":
    run_market_bot()
