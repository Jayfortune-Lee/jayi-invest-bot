import os
import asyncio
import yfinance as yf
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 업무 관련 키워드로 뉴스 수집
    search_keywords = ["Automotive Supply Chain", "Port Logistics", "Global Shipping News"]
    news_data = ""
    try:
        for kw in search_keywords:
            search = yf.Search(kw, max_results=2)
            for news in search.news:
                news_data += f"- {news['title']} ({news.get('publisher', 'Unknown')})\n"
    except Exception as e:
        news_data = "뉴스 데이터를 가져오는 중 일시적인 오류가 발생했습니다."

    prompt = f"""
    당신은 자동차 AS 부품 공급망 관리자입니다. 아래 뉴스를 바탕으로 업무 브리핑을 작성하세요.
    
    [최신 뉴스 데이터]
    {news_data}
    
    [분석 요청]
    1. 주요 권역별(미국, 유럽, 중국, 중동) 정세 리스크 요약.
    2. 항만 파업, 물류 지연 등 AS 부품 수급에 영향을 줄 요인 분석.
    3. 업무 우선순위 및 대응 가이드 제안.
    """
    
    report = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"🚛 **Market Jayi: 업무 리스크 브리핑**\n\n{report}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
