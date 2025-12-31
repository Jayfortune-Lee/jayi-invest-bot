import os
import asyncio
import yfinance as yf
from core.google_sheet import get_portfolio_data
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 1. 구글 시트 데이터 로드
    portfolio = get_portfolio_data()
    
    # 2. 실시간 시세 결합
    pf_analysis = ""
    for stock in portfolio:
        ticker = stock['Ticker']
        avg_price = stock['Avg_Price']
        qty = stock['Quantity']
        
        info = yf.Ticker(ticker).fast_info
        current_price = info['last_price']
        profit_rate = ((current_price - avg_price) / avg_price) * 100
        
        pf_analysis += f"- {ticker}: 보유 {qty}주, 평단 {avg_price}, 현재가 {current_price:.2f} (수익률: {profit_rate:.2f}%)\n"

    # 3. GPT 분석
    prompt = f"""
    [자산 관리 리포트] 아래 포트폴리오를 분석하세요.
    
    {pf_analysis}
    
    [요청 사항]
    1. 현재 거시 경제 상황과 종목별 상관관계 분석.
    2. 익절/손절이 필요한 종목 추천 및 이유.
    3. 포트폴리오 리밸런싱 전략 (자동차 섹터 비중 고려).
    """
    
    report = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"💰 **Wealth Jayi: 자산 관리 리포트**\n\n{report}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
