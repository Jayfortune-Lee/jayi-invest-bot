import os
import asyncio
import pandas as pd
import yfinance as yf
from core.analyzer import ask_gpt
from telegram import Bot
from telegram.request import HTTPXRequest

def get_google_sheet_data():
    """
    구글 시트의 공개된 CSV 링크를 통해 데이터를 읽어옵니다.
    시트에서 [파일] -> [공유] -> [웹에 게시] -> [CSV]로 설정한 URL이 필요합니다.
    """
    sheet_url = os.getenv("GSHEET_URL") # 환경변수에 구글 시트 CSV URL 등록 필수
    try:
        df = pd.read_csv(sheet_url)
        return df
    except Exception as e:
        print(f"시트 로드 실패: {e}")
        return None

async def main():
    df = get_google_sheet_data()
    
    if df is None or df.empty:
        portfolio_summary = "현재 포트폴리오 데이터가 비어있습니다. 구글 시트를 확인해주세요."
    else:
        portfolio_summary = "현재 내 포트폴리오 상황:\n"
        for _, row in df.iterrows():
            ticker = row['종목코드'] # 예: 005930.KS
            stock = yf.Ticker(ticker)
            current_price = stock.fast_info['last_price']
            avg_price = row['평단가']
            qty = row['수량']
            revenue = (current_price - avg_price) * qty
            return_rate = ((current_price / avg_price) - 1) * 100
            
            portfolio_summary += (
                f"- {row['종목명']}({ticker}): 현재가 {current_price:,.0f}원 "
                f"(수익률: {return_rate:.2f}%, 손익: {revenue:,.0f}원)\n"
            )

    role = "당신은 자산 100억을 운용하는 냉철한 펀드매니저입니다. 수익률에 따라 '손절/홀딩/불타기'를 단호하게 결정합니다."
    
    prompt = f"""
    {portfolio_summary}
    
    위 포트폴리오를 분석하여 다음을 수행하세요:
    1. 각 종목에 대해 [매도], [보유], [추매] 의견을 내고 이유를 설명할 것.
    2. 현재 시장 상황(국내외 금리, 업황)을 고려한 리스크 관리 조언.
    3. 전체 자산 중 비중이 너무 높은 종목에 대한 경고.
    """
    
    analysis = ask_gpt(prompt, system_role=role)

    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"), request=t_request)
    
    await bot.send_message(
        chat_id=os.getenv("TG_ID"), 
        text=f"💰 **Wealth Jayi: 수익 전략**\n\n{analysis}", 
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    asyncio.run(main())
