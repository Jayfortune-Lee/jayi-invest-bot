import os
import yfinance as yf
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

portfolio = [
    {"name": "영풍", "ticker": "000670.KQ", "avg_price": 60435, "quantity": 1453, "note": "경영권 분쟁"},
    {"name": "롯데손해보험", "ticker": "000400.KQ", "avg_price": 2008, "quantity": 30000, "note": "매각 이슈"},
    {"name": "동아에스티", "ticker": "170900.KQ", "avg_price": 54487, "quantity": 65, "note": "신약 파이프라인"},
    {"name": "노보노디스크", "ticker": "NVO", "avg_price": 48.59, "quantity": 135, "note": "비만약 특허"},
    {"name": "아마존", "ticker": "AMZN", "avg_price": 230.8572, "quantity": 29, "note": "AI / AWS"}
]

def get_stock_price(ticker):
    data = yf.Ticker(ticker).history(period="1d")
    return data['Close'].iloc[-1]

def analyze_portfolio():
    msg = "📈 개인 주식 포트폴리오 전략\n"
    for stock in portfolio:
        current_price = get_stock_price(stock["ticker"])
        pnl = (current_price - stock["avg_price"]) / stock["avg_price"] * 100
        action = ""
        # 손절 최소화 전략, 익절 시 일부 자금 재투자 추천
        if pnl > 5:
            action = f"부분 익절 → 성장/글로벌 섹터 재투자 (추천 종목: 삼성전자, SK하이닉스, 테슬라, 엔비디아)"
        elif pnl < -10:
            action = f"보유 유지, 시장 모니터링"
        else:
            action = f"보유 유지"
        msg += f"• {stock['name']} ({stock['note']}): {pnl:.2f}% → {action}\n"
    return msg
