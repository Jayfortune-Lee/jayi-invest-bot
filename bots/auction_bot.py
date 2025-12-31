import os
import asyncio
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 분석할 타겟 지역 및 조건
    target_info = "서울 7개구(강남, 서초 등), 84㎡ 이상, 15억 이하 아파트 경매"
    
    # 임시 매물 데이터 (추후 크롤링 결과가 이곳에 들어갑니다)
    sample_item = "사건번호 2023타경102XXX, 서초구 아파트, 감정가 18억, 최저가 14.4억(1회 유찰)"

    prompt = f"""
    [경매 매물 분석]
    관심 조건: {target_info}
    현재 매물: {sample_item}
    
    [분석 내용]
    1. 권리분석(말소기준권리 등 점검) 결과 안전성 평가.
    2. 주변 실거래가 대비 최저가 매력도.
    3. 추천 입찰가 (시세 대비 88% 수준 및 유찰 현황 반영).
    """
    
    report = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"🏠 **Auction Jayi: 경매 추천 매물**\n\n{report}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
