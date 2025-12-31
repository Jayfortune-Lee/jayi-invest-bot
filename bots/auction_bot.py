import os, asyncio, requests
from bs4 import BeautifulSoup
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 실제 구현 시에는 특정 경매 포털 URL 크롤링 로직이 들어갑니다.
    # 여기서는 샘플 데이터로 GPT 권리분석 로직을 구현합니다.
    sample_auction = "강남구 삼성동 OO아파트, 84㎡, 감정가 18억, 최저가 14.4억, 대항력 있는 임차인 없음"
    
    prompt = f"""
    [경매 분석 요청] 서울 주요 지역 매물 권리분석
    - 관심지역: 강남, 서초, 동작, 용산, 송파, 성동, 광진
    - 물건: {sample_auction}
    - 권리분석(안전성), 시세 대비 입찰가(88% 기준 보정), 최종 투자 의견을 작성해줘.
    """
    report = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"🏠 **Auction Jayi: 매물 분석**\n\n{report}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
