import os
import asyncio
import yfinance as yf
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 현대자동차와 직접적으로 관련된 키워드로 고도화
    search_keywords = [
        "Hyundai Motor Global Sales", 
        "Hyundai Supply Chain Risk", 
        "Automotive Spare Parts Logistics",
        "Competitor Analysis BYD Tesla"
    ]
    
    news_data = ""
    try:
        for kw in search_keywords:
            search = yf.Search(kw, max_results=2)
            for news in search.news:
                news_data += f"- {news['title']} ({news.get('publisher', 'Unknown')})\n"
    except Exception as e:
        news_data = "뉴스 데이터를 읽어오는 중 일부 오류가 발생했습니다."

    prompt = f"""
    [현대자동차 재직자 전용 업무 리스크 보고서]
    
    최근 수집된 뉴스:
    {news_data}
    
    위 데이터를 바탕으로 다음 내용을 분석하세요:
    1. 글로벌 시장(미국/유럽/인도 등)에서 현대차의 입지에 영향을 줄 최신 리스크.
    2. 현대차 및 제네시스 브랜드의 AS 부품 공급망(Logistics)에 예상되는 병목 현상.
    3. 경쟁사(테슬라, 토요타, BYD)의 동향 중 현대차 재직자가 긴급히 참고해야 할 사항.
    4. 오늘 업무에서 우선적으로 점검해야 할 '현대차 맞춤형' 대응 가이드.
    """
    
    report = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"))
    await bot.send_message(
        chat_id=os.getenv("TG_ID"), 
        text=f"🚙 **Hyundai Jayi: 현대차 업무 리포트**\n\n{report}", 
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    asyncio.run(main())
