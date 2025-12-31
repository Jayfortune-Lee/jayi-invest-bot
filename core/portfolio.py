from core.macro import get_macro_news

def get_stock_news(ticker, limit=1):
    news_list = get_macro_news(f"{ticker} 주식 OR {ticker} 뉴스", limit=limit)
    return " | ".join([f"[{t}]({l})" for t, l in news_list]) if news_list else "관련 뉴스 없음"

def get_portfolio_message():
    portfolio = [
        {"name": "영풍", "issue": "경영권 분쟁", "pnl": -21.4,
         "strategy": "손절 최소화, 장기 관점", "reinvest": ["삼성SDI", "LG에너지솔루션"]},
        {"name": "롯데손해보험", "issue": "매각 이슈", "pnl": -13.4,
         "strategy": "보유 유지, 뉴스 모니터링", "reinvest": []},
        {"name": "동아에스티", "issue": "신약 파이프라인", "pnl": -3.6,
         "strategy": "장기 보유, 손절 없음", "reinvest": []},
        {"name": "노보노디스크", "issue": "비만약 특허", "pnl": 5.4,
         "strategy": "목표 수익률 10% 도달 시 일부 익절",
         "reinvest": ["마이크로소프트", "엔비디아", "존슨앤존슨", "화이자"]},
        {"name": "아마존", "issue": "AI / AWS", "pnl": 0.7,
         "strategy": "장기 성장 관점 유지",
         "reinvest": ["MS", "구글", "AI 관련 ETF"]}
    ]

    lines = ["📈 개인 주식 포트폴리오 전략 브리핑\n━━━━━━━━━━━━━━━━━━"]
    for p in portfolio:
        reinvest_str = f" → 익절 후 재투자 추천: {', '.join(p['reinvest'])}" if p['reinvest'] else ""
        news_str = get_stock_news(p['name'])
        line = f"• {p['name']} ({p['issue']}): {p['pnl']}% → {p['strategy']}{reinvest_str} | 뉴스: {news_str}"
        lines.append(line)
    return "\n".join(lines)
