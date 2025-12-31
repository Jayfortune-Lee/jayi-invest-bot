import os
import asyncio
import yfinance as yf
from core.google_sheet import get_portfolio_data
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    portfolio = get_portfolio_data()
    
    pf_details = ""
    total_buy = 0
    total_curr = 0

    for stock in portfolio:
        ticker_raw = stock.get('Ticker') or stock.get('ticker')
        avg_price = stock.get('Avg_Price') or stock.get('avg_price')
        qty = stock.get('Quantity') or stock.get('quantity')
        
        if not ticker_raw: continue
        ticker = str(ticker_raw).strip()

        try:
            s = yf.Ticker(ticker)
            current_price = s.fast_info['last_price']
            
            buy_amt = float(avg_price) * int(qty)
            curr_amt = current_price * int(qty)
            profit_rate = ((current_price - float(avg_price)) / float(avg_price)) * 100
            
            total_buy += buy_amt
            total_curr += curr_amt

            pf_details += f"- {ticker}: 현재가 {current_price:,.0f} (수익률 {profit_rate:+.2f}%)\n"
        except:
            pf_details += f"- {ticker}: 시세 로드 실패\n"

    total_rate = ((total_curr - total_buy) / total_buy) * 100 if total_buy > 0 else 0
    summary = (f"💰 **수익 현황 보고**\n"
               f"- 총 매수: {total_buy:,.0f}원\n"
               f"- 평가액: {total_curr:,.0f}원\n"
               f"- 수익률: {total_rate:+.2f}%\n\n"
               f"📈 **보유 종목**\n{pf_details}")

    # GPT에게 오직 '돈'을 기준으로 분석 요청
    prompt = f"""
    [투자 자산 데이터]
    {summary}
    
    [분석 지시]
    당신은 냉혹한 전업 투자자입니다. 위 포트폴리오의 수익률을 극대화하기 위한 전략만 제시하세요.
    1. 각 종목별 주가에 영향을 줄 '돈 되는 뉴스' 요약.
    2. 현재 손익률 기준, 기회비용을 따져서 '손절/익절/추매'를 숫자 기반으로 제안.
    3. 현재 거시경제 상황에서 가장 수익 확률이 높은 유망 섹터 1개 추천.
    조언은 짧고 단호하게 하세요.
    """
    
    analysis = ask_gpt(prompt)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"{summary}\n\n📍 **수익 전략**\n{analysis}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
