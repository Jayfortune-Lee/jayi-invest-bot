from core.macro import fetch_global_car_as_news
from core.portfolio import analyze_portfolio
from telegram_sender import send_telegram_message

def run_market_bot():
    macro_msg = fetch_global_car_as_news()
    portfolio_msg = analyze_portfolio()
    final_msg = f"📅 오늘의 전략 브리핑\n━━━━━━━━━━━━━━━━━━\n{macro_msg}\n\n{portfolio_msg}"
    send_telegram_message(final_msg)

if __name__ == "__main__":
    run_market_bot()
