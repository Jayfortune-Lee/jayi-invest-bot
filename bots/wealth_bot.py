import os, asyncio
import yfinance as yf
from core.google_sheet import get_portfolio_data
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    portfolio = get_portfolio_data()
    pf_str = ""
    for p in portfolio:
        current = yf.Ticker(p['Ticker']).fast_info['last_price']
        profit = ((current - p['Avg_Price']) / p['Avg_Price']) * 100
        pf_str += f"- {p['Ticker']}: {p['Quantity']}주, 수익률 {profit:.2f}%\n"

    prompt = f"""
    [자산 관리 요청] 내 포트폴리오 분석 및 리밸런싱
    - 현황: {pf_str}
    - 현재 거시 경제(금리, 환율)를 반영한 시장 분석.
    - 개별 종목 익절/손절 전략 및 글로벌 성장 섹터 재투자 추천.
    - 포트폴리오 위험도 평가 및 비중 조절 제안.
    """
    report = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"💰 **Wealth Jayi: 자산 리포트**\n\n{report}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
