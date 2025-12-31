import os
import asyncio
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 1. 샘플 매물 데이터 (서울 주요 지역 사례)
    # 실제 운영 시에는 이 리스트에 여러 매물을 넣을 수 있습니다.
    auction_items = [
        {
            "case_no": "2023타경108XXX",
            "location": "서울시 송파구 가락동 가락금호 84㎡",
            "appraisal_value": 1500000000, 
            "min_bid_price": 1200000000,   
            "status": "유찰 1회",
            "market_price": 1420000000,
            "is_occupied_by_owner": True   # 소유자 거주 여부 등 특이사항
        },
        {
            "case_no": "2024타경205XXX",
            "location": "서울시 노원구 상계동 상계주공 59㎡",
            "appraisal_value": 700000000, 
            "min_bid_price": 448000000,   
            "status": "유찰 2회",
            "market_price": 620000000,
            "is_occupied_by_owner": False
        }
    ]

    items_text = ""
    for item in auction_items:
        items_text += (f"- 사건번호: {item['case_no']}\n"
                       f"  위치: {item['location']}\n"
                       f"  감정가: {item['appraisal_value']:,.0f}원\n"
                       f"  최저가: {item['min_bid_price']:,.0f}원 ({item['status']})\n"
                       f"  인근시세: {item['market_price']:,.0f}원\n\n")

    # 2. GPT에게 투자/실거주 구분 및 수익 분석 요청
    role = "당신은 경매 경력 20년의 실전 부동산 전문가입니다. 모든 매물을 '투자용'과 '실거주용'으로 명확히 구분하여 가치를 평가합니다."
    
    prompt = f"""
    [서울 아파트 경매 매물 분석]
    {items_text}
    
    [분석 요청]
    1. 각 매물에 대해 **[투자용]** 또는 **[실거주용]** 딱지를 붙여주세요. (둘 다 해당되면 이유 설명)
    2. **투자용**인 경우: 전세가율과 시세 차익(Margin)을 바탕으로 한 단기 수익성 분석.
    3. **실거주용**인 경우: 입지, 학군, 실거주 편의성 및 경매를 통해 급매보다 싸게 사는 전략 분석.
    4. 각 매물별 '절대 놓치지 말아야 할 적정 입찰가'를 숫자로 제시하세요.
    """
    
    analysis = ask_gpt(prompt, system_role=role)
    
    # 3. 텔레그램 전송
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    await bot.send_message(
        chat_id=os.getenv("TG_ID"), 
        text=f"🏠 **Auction Jayi: 실전 경매 브리핑**\n\n{analysis}", 
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    asyncio.run(main())
