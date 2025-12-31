import os
import asyncio
from core.crawler import get_seoul_auction_items
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    auction_items = get_seoul_auction_items()
    
    if not auction_items:
        print("해당 지역에 신규 유찰 매물이 없습니다.")
        return

    items_summary = ""
    for item in auction_items:
        items_summary += (
            f"📍 [{item['district']}] {item['title']}\n"
            f"- 사건번호: {item['case_no']}\n"
            f"- 가격: 감정 {item['appraisal_value']:,.0f} / 최저 {item['min_bid_price']:,.0f}\n"
            f"- 상태: {item['status']} | 시세: {item['market_price']}\n"
            f"- 포인트: {item['description']}\n\n"
        )

    role = "당신은 서울 상급지 전문 부동산 투자 고수입니다. 오직 핵심지 매물의 가치와 수익성만 평가합니다."
    
    prompt = f"""
    [핵심 지역 경매 분석 리스트]
    {items_summary}
    
    위 매물들은 사용자가 지정한 '서울 핵심 9개구'의 매물입니다. 다음 룰에 따라 분석하세요.
    
    1. **분류**: 각 매물에 **[투자용]** 또는 **[실거주용]** 딱지를 붙이고 그 이유를 단지의 미래 가치와 연계하여 설명할 것.
    2. **수익률 룰링**: 최저가 낙찰 시 예상되는 시세 차익(Margin)을 계산하고, 취득세 및 대출 이자를 고려했을 때 '남는 장사'인지 판단할 것.
    3. **입지 분석**: 해당 구 내에서도 해당 단지가 갖는 입지적 우위(교통, 학군, 개발호재)를 짚어줄 것.
    4. **최종 픽**: 오늘 리스트 중 가장 '돈 냄새' 나는 단지 하나를 골라 목표가와 함께 추천할 것.
    """
    
    analysis = ask_gpt(prompt, system_role=role)
    
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    message = f"🏢 **Auction Jayi: 핵심 지역 경매 룰링**\n\n{analysis}"
    
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=message, parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
