import os
import asyncio
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 1. 실제 시장 데이터를 기반으로 한 상세 매물 리스트 (샘플 양 대폭 확대)
    # 나중에 이 부분을 크롤링 함수로 대체하면 실시간으로 바뀝니다.
    auction_items = [
        {
            "case_no": "2023타경111234",
            "title": "송파구 잠실동 리센츠 84㎡",
            "details": "층수: 15/25층 | 대지권: 40㎡ | 보존등기: 2008년",
            "appraisal_value": 2500000000, 
            "min_bid_price": 2000000000,   
            "status": "유찰 1회 (20% 저감)",
            "market_price": "실거래가 24.5억 수준",
            "features": "엘스/트리지움과 함께 잠실 대장주. 단지 내 초중고 보유. 토지거래허가구역 제외(경매 특전)."
        },
        {
            "case_no": "2024타경5678",
            "title": "노원구 상계동 상계주공 5단지 37㎡",
            "details": "층수: 3/5층 | 재건축 추진 중 | 대지지분 높음",
            "appraisal_value": 700000000, 
            "min_bid_price": 448000000,   
            "status": "유찰 2회 (36% 저감)",
            "market_price": "급매 6억 수준",
            "features": "재건축 정밀안전진단 통과. 소액 투자 가능. 미래 가치 높음."
        }
    ]

    items_text = ""
    for item in auction_items:
        items_text += (f"📍 [사건번호: {item['case_no']}]\n"
                       f"🏢 매물: {item['title']}\n"
                       f"📝 상세: {item['details']}\n"
                       f"💰 가격: 감정가 {item['appraisal_value']:,.0f}원 / 최저가 {item['min_bid_price']:,.0f}원\n"
                       f"📉 현황: {item['status']} | 시세: {item['market_price']}\n"
                       f"🌟 특징: {item['features']}\n\n")

    # 2. GPT에게 아주 깐깐하게 분석 요청
    role = "당신은 수익률에 미친 1타 부동산 경매 강사이자 전업 투자자입니다. 부실한 정보는 취급하지 않으며, 숫자로 증명된 수익성만 논합니다."
    
    prompt = f"""
    [오늘의 필터링된 서울 아파트 경매 리스트]
    {items_text}
    
    위 매물들에 대해 다음을 포함하여 '돈 냄새 나는' 리포트를 작성하세요:
    
    1. **용도 분류**: [투자용] 또는 [실거주용] 딱지를 붙이고 근거를 제시할 것.
    2. **권리분석**: 대항력 있는 임차인 유무, 인수될 수 있는 권리 등 위험 요소를 경고할 것.
    3. **수익성 계산**: '낙찰가 - 시세 - 취등록세/명도비'를 고려한 예상 순수익 계산.
    4. **입찰 전략**: 현재 유찰 상태에서 이번 차수에 들어가는 게 맞는지, 한 번 더 기다려야 하는지 명확히 결정할 것.
    5. **최종 픽**: 오늘 리스트 중 '가장 돈이 될 매물' 하나를 골라 목표 수익을 제시할 것.
    
    전문적인 부동산 용어를 사용하되 가독성 좋게 작성하세요.
    """
    
    analysis = ask_gpt(prompt, system_role=role)
    
    # 3. 전송
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    await bot.send_message(
        chat_id=os.getenv("TG_ID"), 
        text=f"🏠 **Auction Jayi: 돈 되는 경매 분석**\n\n{analysis}", 
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    asyncio.run(main())
