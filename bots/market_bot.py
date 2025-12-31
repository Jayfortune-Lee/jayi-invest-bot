import os
from openai import OpenAI
from core.portfolio import get_portfolio_brief
from core.macro import get_macro_brief
from core.telegram_sender import send_telegram_message

def run_market_bot():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # 글로벌 자동차/AS 시장 브리핑
    macro_text = get_macro_brief()

    # 개인 포트폴리오 브리핑
    portfolio_text = get_portfolio_brief(client)

    # 텔레그램 메시지 전송
    message = f"📅 오늘의 전략 브리핑\n━━━━━━━━━━━━━━━━━━\n"
    message += macro_text + "\n━━━━━━━━━━━━━━━━━━\n" + portfolio_text

    chat_id = os.environ.get("TG_ID_MARKET")
    send_telegram_message(chat_id, message)

if __name__ == "__main__":
    run_market_bot()
