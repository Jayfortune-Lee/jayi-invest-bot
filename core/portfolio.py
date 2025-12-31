import openai
import os
import yfinance as yf

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

portfolio = {
    "영풍": {"avg_price": 60435, "quantity": 1453, "info": "경영권 분쟁"},
    "롯데손해보험": {"avg_price": 2008, "quantity": 30000, "info": "매각 이슈"},
    "동아에스티": {"avg_price": 54487, "quantity": 65, "info": "신약 파이프라인"},
    "노보노디스크": {"avg_price": 48.59, "quantity": 135, "info": "비만약 특허"},
    "아마존": {"avg_price": 230.8572, "quantity": 29, "info": "AI / AWS"}
}

def get_current_price(ticker):
    try:
        price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
        return price
    except:
        return None

def generate_portfolio_brief():
    """
    보유 종목별로 익절/손절/보유 전략과 재투자 추천 포함
    """
    openai.api_key = OPENAI_API_KEY
    messages = [{"role":"user","content":f"주식 포트폴리오: {portfolio}. "
                "각 종목별 현재 시세, 특이사항 반영한 익절/손절/보유 전략, "
                "추가 재투자 종목 추천, 글로벌/한국 경제 영향 포함한 실전 투자 전략으로 브리핑."}]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.6
    )
    analysis = response['choices'][0]['message']['content']
    return analysis
