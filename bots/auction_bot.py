from core.auction import fetch_seoul_auction, analyze_auction
from telegram_sender import send_telegram_message

def run_auction_bot():
    apartments = fetch_seoul_auction()
    if not apartments:
        send_telegram_message("오늘 경매 매물 없음")
        return
    messages = [analyze_auction(apt) for apt in apartments]
    send_telegram_message("📌 오늘 서울 경매 매물\n━━━━━━━━━━━━━━━━━━\n" + "\n".join(messages))

if __name__ == "__main__":
    run_auction_bot()
