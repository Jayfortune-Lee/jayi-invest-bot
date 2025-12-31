from core.macro import fetch_global_car_as_news
from core.portfolio import generate_portfolio_brief
from telegram_sender import send_telegram_message
import os

BOT_TOKEN = os.getenv("TG_TOKEN_MARKET")
CHAT_ID = os.getenv("TG_ID_MARKET")

def run_market_bot():
    macro = fetch_global_car_as_news()
    portfolio = generate_portfolio_brief()
    message = f"📅 오늘의 전략 브리핑\n━━━━━━━━━━━━━━━━━━\n🚗 글로벌 자동차/AS 시장\n{macro}\n\n📈 개인 포트폴리오\n{portfolio}"
    send_telegram_message(BOT_TOKEN, CHAT_ID, message)

if __name__ == "__main__":
    run_market_bot()
