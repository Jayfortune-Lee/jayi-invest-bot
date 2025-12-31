import os
import asyncio
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 1. 타겟 매물 데이터 (실제 서비스 연동 전, 현재 수익성 높은 표본 매물 설정)
    # 추후 크롤러가 완성되면 이 변수에 실시간 데이터가 들어갑니다.
    auction_items = [
        {
            "case_no": "2023타경108XXX",
            "location": "서울시 송파구 가락동 XXX 아파트",
            "appraisal_value": 1500000000, # 감정가 15억
            "min_bid_price": 1200000000,   # 최저가 12억 (1회 유찰)
            "status": "유찰 1회",
            "market_price": 1450000000     # 인근 실거래가 약 14.5억
        }
    ]

    items_text = ""
    for item in auction_items:
        items_text += (f"- 사건번호: {item['case_no']}\n"
                       f"  위치: {item['location']}\n"
                       f"  감정가: {item['appraisal_value']:,.0f}원\n"
                       f"  최저가: {item['min_bid_price']:,.0f}원 ({item['status']})\n"
                       f"  인근시세: {item['market_price']:,.0f}원\n\n")

    # 2. GPT에게 '돈'을 기준으로 분석 요청
    role = "당신은 100억 자산가이자 대한민국 최고의 경매 컨설턴트입니다. 오직 경락 잔금 대출 효율과 시세 차익(Margin)만 봅니다."
    
    prompt = f"""
    [오늘의 서울 아파트 경매 분석 대상]
    {items_text}
    
    [분석 지시]
    1. 위 매물 중 가장 '돈이 되는' 매물을 선정하고 이유를 시세 차익 위주로 설명하세요.
    2. 권리분석 시 주의해야 할 점(대항력 있는 임차인, 인수 금액 등)을 냉정하게 지적하세요.
    3. 인근 실거래가 대비 몇 % 수준에서 입찰해야 수익이 극대화될지 구체적인 '입찰 추천가'를 제시하세요.
    """
    
    analysis = ask_gpt(prompt, system_role=role)
    
    # 3. 텔레그램 전송
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    await bot.send_message(
        chat_id=os.getenv("TG_ID"), 
        text=f"🏠 **Auction Jayi: 경매 수익 분석**\n\n{analysis}", 
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    asyncio.run(main())
