# 주식 포트폴리오 분석
import yfinance as yf

PORTFOLIO = {
    "영풍": {"ticker": "000670.KS", "avg": 60435, "qty": 1453, "issue": "경영권 분쟁"},
    "롯데손해보험": {"ticker": "000400.KS", "avg": 2008, "qty": 30000, "issue": "매각 이슈"},
    "동아에스티": {"ticker": "170900.KS", "avg": 54487, "qty": 65, "issue": "신약 파이프라인"},
    "노보노디스크": {"ticker": "NVO", "avg": 48.59, "qty": 135, "issue": "비만약 특허"},
    "아마존": {"ticker": "AMZN", "avg": 230.8572, "qty": 29, "issue": "AI / AWS"}
}

def get_price(ticker):
    data = yf.Ticker(ticker).history(period="1d")
    return float(data["Close"].iloc[-1])

def analyze_portfolio():
    result = []
    for name, info in PORTFOLIO.items():
        price = get_price(info["ticker"])
        pnl = (price - info["avg"]) / info["avg"] * 100

        if pnl >= 25:
            action = "부분 익절 → 성장 섹터 리밸런싱"
        elif pnl <= -20:
            action = "손절 검토 → 대체 자산 이동"
        else:
            action = "보유 유지"

        result.append(
            f"• {name} ({info['issue']}): {pnl:.1f}% → {action}"
        )

    return "\n".join(result)
