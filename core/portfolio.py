import openai
import os
import yfinance as yf
import pandas as pd

openai.api_key = os.environ.get("OPENAI_API_KEY")

# 보유 주식
portfolio = [
    {"ticker":"영풍", "avg_price":60435, "qty":1453, "note":"경영권 분쟁"},
    {"ticker":"롯데손해보험", "avg_price":2008, "qty":30000, "note":"매각 이슈"},
    {"ticker":"동아에스티", "avg_price":54487, "qty":65, "note":"신약 파이프라인"},
    {"ticker":"NVO", "avg_price":48.59, "qty":135, "note":"비만약 특허"},   # 노보노디스크
    {"ticker":"AMZN", "avg_price":230.8572, "qty":29, "note":"AI/AWS"}   # 아마존
]

def fetch_current_price(ticker):
    if ticker in ["NVO","AMZN"]:
        return yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
    else:
        # 국내 주식 가격 API 연결 필요 (예: 네이버 금융, Open API 등)
        return None

def auto_portfolio_brief():
    # 현재 포트폴리오 상태와 익절/재투자 추천
    summary = "📈 개인 주식 포트폴리오\n"
    for p in portfolio:
        current = fetch_current_price(p["ticker"])
        if current:
            gain = (current - p["avg_price"]) / p["avg_price"] * 100
        else:
            gain = 0  # 예시
        summary += f"• {p['ticker']} ({p['note']}): {gain:.2f}% → "
        if gain > 5:
            summary += f"부분 익절, 성장/글로벌 섹터 재투자 추천\n"
        elif gain < -15:
            summary += "보수적 접근, 일부 손절 고려\n"
        else:
            summary += "보유 유지, 관찰\n"
    return summary
