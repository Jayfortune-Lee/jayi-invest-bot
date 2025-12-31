import os
import asyncio
from core.crawler import get_seoul_auction_items
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    auction_items = get_seoul_auction_items()
    
    if not auction_items:
        return

    items_summary = ""
    for item in auction_items:
        # 네이버 경매 검색 링크 생성 (사건번호 기반)
        # 보통 검색창에 사건번호를 치면 바로 나오기 때문에 검색 결과 페이지 링크를 활용합니다.
        search_url = f"https://land.naver.com/auction/search.naver?query={item['case_no']}"
        
        items_summary += (
            f"📍 [{item['district']}] {item['title']}\n"
            f"- 사건번호: {item['case_no']}\n"
            f"- 가격: 감정 {item['appraisal_value']:,.0f} / 최저 {item['min_bid_price']:,.0f}\n"
            f"- 포인트: {item['description']}\n"
            f"🔗 [매물 정보 확인하기]({search_url})\n\n" # 이 부분이 링크가 됩니다.
        )

    role = "당신은 실전 경매 전문가입니다. 매물 분석 시 반드시 [투자용/실거주용] 딱지를 붙이고, 사용자가 직접 검토할 수 있도록 사건번호와 위치를 정확히 안내하세요."
    
    prompt = f"""
    [핵심 지역 경매 리스트]
    {items_summary}
    
    위 리스트에 대해 다음을 수행하세요:
    1. 각 매물별로 [투자용/실거주용] 분류 및 상세 수익 분석.
    2. 입찰 시 주의사항(권리분석 특이사항).
    3. 각 분석 내용 끝에 '위의 매물 확인 링크를 클릭하여 사진과 등기를 확인하세요'라는 멘트를 넣을 것.
    """
    
    analysis = ask_gpt(prompt, system_role=role)
    
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    # 분석글과 링크를 결합
    final_message = f"🏠 **Auction Jayi: 실전 경매 브리핑**\n\n{analysis}\n\n--- \n📌 **검토용 매물 리스트**\n{items_summary}"
    
    # MarkdownV2를 쓰면 링크가 깔끔하게 걸립니다. (여기선 기본 Markdown 사용)
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=final_message, parse_mode="Markdown", disable_web_page_preview=False)

if __name__ == "__main__":
    asyncio.run(main())
