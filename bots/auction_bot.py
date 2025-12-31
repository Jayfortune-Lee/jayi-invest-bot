import os
import asyncio
from core.crawler import get_seoul_auction_items # 크롤러 불러오기
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 1. 크롤러로부터 매물 데이터 수집
    auction_items = get_seoul_auction_items()
    
    items_summary = ""
    for item in auction_items:
        items_summary += (
            f"🏠 {item['title']} ({item['case_no']})\n"
            f"- 감정가: {item['appraisal_value']:,.0f}원\n"
            f"- 최저가: {item['min_bid_price']:,.0f}원 ({item['status']})\n"
            f"- 시세: {item['market_price']}\n"
            f"- 특징: {item['description']}\n\n"
        )

    # 2. GPT에게 독설 섞인 투자 분석 요청
    role = "당신은 경매로만 100억을 번 실전 부동산 투자의 귀재입니다. 돈 안 되는 매물은 가차 없이 까버립니다."
    
    prompt = f"""
    [오늘의 서울 아파트 경매 분석 리스트]
    {items_summary}
    
    위 매물들을 분석하여 다음 형식으로 리포트를 작성하세요.
    
    1. 각 매물별로 **[투자용]** 또는 **[실거주용]** 분류 (이유 포함).
    2. 수익률 분석: 최저가에 낙찰 시 예상되는 시세 차익과 세후 수익 추정.
    3. 위험 경고: 권리상 인수될 금액이 있는지(대항력 등) 주의사항 언급.
    4. 최종 결론: "오늘 반드시 입찰해야 할 원픽 매물"과 추천 입찰가 제안.
    """
    
    analysis = ask_gpt(prompt, system_role=role)
    
    # 3. 텔레그램 전송
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    message = f"📢 **Auction Jayi 실전 경매 리포트**\n\n{analysis}"
    
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=message, parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
