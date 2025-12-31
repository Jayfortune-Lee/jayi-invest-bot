import os
import asyncio
from core.crawler import get_seoul_auction_items
from core.analyzer import ask_gpt
from telegram import Bot
from telegram.request import HTTPXRequest

async def main():
    # 1. 크롤러 데이터 가져오기
    auction_items = get_seoul_auction_items()
    
    # 텔레그램 설정 (타임아웃 방지 추가)
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"), request=t_request)
    chat_id = os.getenv("TG_ID")

    # [중요] 매물이 없을 경우 사용자에게 알림을 보내도록 수정
    if not auction_items:
        await bot.send_message(
            chat_id=chat_id, 
            text="📢 **Auction Jayi 알림**\n\n현재 설정하신 '서울 핵심 9개구 + 15억 이하' 조건에 맞는 신규 유찰 매물이 없습니다. 내일 다시 확인하겠습니다!"
        )
        return

    # 2. 매물이 있을 경우 분석 진행
    analysis_input = ""
    link_section = "📌 **실제 매물 검토 링크**\n\n"

    for item in auction_items:
        search_url = f"https://land.naver.com/auction/search.naver?query={item['case_no']}"
        analysis_input += (
            f"📍 [{item['district']}] {item['title']}\n"
            f"- 사건번호: {item['case_no']}\n"
            f"- 금액: 감정 {item['appraisal_value']:,.0f} / 최저 {item['min_bid_price']:,.0f}\n"
            f"- 특징: {item['description']}\n\n"
        )
        link_section += f"🏠 **{item['title']}**\n👉 [사건번호 검색]({search_url})\n\n"

    role = "당신은 15억 이하 서울 상급지 아파트만 공략하는 실전 경매 고수입니다."
    prompt = f"아래 매물을 분석하여 [투자용/실거주용] 분류와 예상 수익을 짧고 굵게 리포트하세요:\n{analysis_input}"
    
    analysis_result = ask_gpt(prompt, system_role=role)
    
    final_message = f"🏠 **Auction Jayi: 실전 룰링**\n\n{analysis_result}\n\n{link_section}"
    
    try:
        await bot.send_message(chat_id=chat_id, text=final_message, parse_mode="Markdown")
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=final_message.replace("*", ""))

if __name__ == "__main__":
    asyncio.run(main())
