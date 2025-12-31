import sys
import os

# 현재 파일의 위치를 기준으로 상위 폴더(루트)를 파이썬 경로에 강제로 등록합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 이제 'core'를 확실히 찾을 수 있습니다.
import asyncio
import yfinance as yf
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 업무 리스크 분석 로직
    sectors = ["Global Supply Chain", "Automotive Logistics", "Port Strike"]
    news_context = ""
    try:
        for s in sectors:
            news_context += str(yf.Search(s, max_results=2).news)
    except:
        news_context = "뉴스 데이터를 가져오는 중 오류가 발생했습니다."

    prompt = f"""
    [업무 브리핑] 글로벌 자동차/AS 리스크 분석
    - 뉴스: {news_context}
    - 5대 권역별 정세 및 공급망 리스크 요약.
    - AS 담당자를 위한 실무 가이드.
    """
    report = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"🚛 **Market Jayi: 업무 브리핑**\n\n{report}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
