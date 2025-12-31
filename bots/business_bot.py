import os, asyncio
import yfinance as yf
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 주요 글로벌 뉴스 키워드 수집 (yfinance 뉴스 활용 및 검색어 조합)
    sectors = ["Global Supply Chain", "Automotive Logistics", "Port Strike", "Car Parts Shortage"]
    news_context = ""
    for s in sectors:
        news_context += str(yf.Search(s, max_results=3).news)

    prompt = f"""
    [업무 브리핑 요청] 글로벌 자동차/AS 시장 리스크 분석
    - 수집 뉴스: {news_context}
    - 5대 권역(미국, 중국, 유럽, 중동, 멕시코/동남아)별 정세 및 재난/전쟁 리스크 요약.
    - 특히 OEM 생산 지연이 AS 부품 공급망과 수익성에 미치는 영향 분석.
    - AS 담당자가 오늘 주목해야 할 실무 행동 가이드 제시.
    """
    report = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"🚛 **Market Jayi: 업무 브리핑**\n\n{report}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
