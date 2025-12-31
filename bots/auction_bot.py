import os
import asyncio
from core.crawler import get_seoul_auction_items
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 1. 크롤러 데이터 가져오기
    auction_items = get_seoul_auction_items()
    
    if not auction_items:
        print("조건에 맞는 매물이 없습니다.")
        return

    analysis_input = ""
    link_section = "📌 **직접 검토 및 상세 정보 링크**\n\n"

    for item in auction_items:
        # 검색용 링크 생성
        search_url = f"https://land.naver.com/auction/search.naver?query={item['case_no']}"
        district_url = f"https://land.naver.com/auction/search.naver?query={item['district']}+아파트"
        
        analysis_input += (
            f"📍 [{item['district']}] {item['title']}\n"
            f"- 사건번호: {item['case_no']}\n"
            f"- 금액: 감정 {item['appraisal_value']:,.0f} / 최저 {item['min_bid_price']:,.0f}\n"
            f"- 시세: {item['market_price']}\n"
            f"- 특징: {item['description']}\n\n"
        )
        
        link_section += (
            f"🏠 **{item['title']} ({item['case_no']})**\n"
            f"👉 [사건번호 검색]({search_url}) | [해당 구 전체보기]({district_url})\n\n"
        )

    # 2. GPT 전문가 룰링
    role = "당신은 15억 이하 서울 상급지 아파트만 공략하는 실전 경매 고수입니다. 냉정하고 단호하게 수익성을 평가합니다."
    
    prompt = f"""
    [15억 이하 서울 핵심 매물 리스트]
    {analysis_input}
    
    위 매물들에 대해 다음을 분석하세요:
    1. 각 매물에 **[투자용]** 또는 **[실거주용]** 딱지를 붙일 것.
    2. 시세 대비 낙찰 시 예상되는 실질 순수익금(세전)을 숫자로 제시할 것.
    3. 15억 예산 범위에서 가장 가성비가 높은 '원픽' 매물을 선정할 것.
    4. 분석 끝에 '상세 내용은 하단 링크를 통해 실제 사진과 등기를 확인하십시오'라고 멘트할 것.
    """
    
    analysis_result = ask_gpt(prompt, system_role=role)
    
    # 3. 텔레그램 전송
    final_message = f"🏠 **Auction Jayi: 15억 이하 실전 룰링**\n\n{analysis_result}\n\n{link_section}"
    
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    
    try:
        await bot.send_message(
            chat_id=os.getenv("TG_ID"), 
            text=final_message, 
            parse_mode="Markdown",
            disable_web_page_preview=False
        )
    except Exception:
        # 마크다운 에러 시 일반 텍스트로 재시도
        await bot.send_message(chat_id=os.getenv("TG_ID"), text=final_message.replace("*", ""))

if __name__ == "__main__":
    asyncio.run(main())
