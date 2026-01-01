import os
import asyncio
from core.crawler import get_seoul_auction_items
from core.analyzer import ask_gpt
from telegram import Bot
from telegram.request import HTTPXRequest

async def main():
    # 1. 크롤러 데이터 가져오기 (await 사용)
    auction_items = await get_seoul_auction_items()
    
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"), request=t_request)
    chat_id = os.getenv("TG_ID")

    if not auction_items:
        await bot.send_message(chat_id=chat_id, text="📢 **Auction Jayi**\n조건에 맞는 실시간 매물이 없습니다.")
        return

    analysis_input = ""
    link_section = "📌 **실시간 경매 상세 정보**\n\n"

    for item in auction_items:
        dooin_url = f"https://www.dooinauction.com/auction/search/list.php?search_text={item['case_no']}"
        analysis_input += (
            f"📍 {item['title']}\n"
            f"- 사건번호: {item['case_no']}\n"
            f"- 감정가: {item['appraisal_value']:,.0f}원\n\n"
        )
        link_section += f"🏠 **{item['title']}**\n👉 [상세 정보 확인]({dooin_url})\n\n"

    role = "당신은 15억 이하 서울 아파트 전문 경매 컨설턴트입니다."
    prompt = f"아래 매물들을 실무자 관점에서 분석하세요:\n{analysis_input}"
    
    analysis_result = ask_gpt(prompt, system_role=role)
    final_message = f"🏠 **Auction Jayi: 실시간 룰링**\n\n{analysis_result}\n\n{link_section}"
    
    try:
        await bot.send_message(chat_id=chat_id, text=final_message, parse_mode="Markdown", disable_web_page_preview=True)
    except:
        await bot.send_message(chat_id=chat_id, text=final_message.replace("*", ""))

if __name__ == "__main__":
    asyncio.run(main())
