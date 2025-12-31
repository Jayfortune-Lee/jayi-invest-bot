import os

# 보유 종목 정보 (평균단가, 수량, 특이사항)
portfolio_data = {
    "영풍": {
        "avg_price": 60435,
        "quantity": 1453,
        "issue": "경영권 분쟁",
        "risk_level": "높음",
        "target_profit_pct": 10,  # 목표 수익률 (%)
        "stop_loss_pct": 15       # 손절 기준 (%)
    },
    "롯데손해보험": {
        "avg_price": 2008,
        "quantity": 30000,
        "issue": "매각 이슈",
        "risk_level": "중간",
        "target_profit_pct": 15,
        "stop_loss_pct": 20
    },
    "동아에스티": {
        "avg_price": 54487,
        "quantity": 65,
        "issue": "신약 파이프라인",
        "risk_level": "중간",
        "target_profit_pct": 10,
        "stop_loss_pct": 15
    },
    "노보노디스크": {
        "avg_price": 48.59,  # 달러
        "quantity": 135,
        "issue": "비만약 특허",
        "risk_level": "낮음",
        "target_profit_pct": 10,
        "stop_loss_pct": 8
    },
    "아마존": {
        "avg_price": 230.8572,  # 달러
        "quantity": 29,
        "issue": "AI / AWS 성장",
        "risk_level": "낮음",
        "target_profit_pct": 12,
        "stop_loss_pct": 10
    }
}

# 현재 시세 가져오기 (Yahoo Finance 사용)
import yfinance as yf

def get_current_price(ticker: str) -> float:
    """
    티커명 기준으로 현재 종가 가져오기
    """
    data = yf.Ticker(ticker).history(period="1d")
    if "Close" in data:
        return data["Close"].iloc[-1]
    else:
        return 0

# 티커 매핑 (한국주식은 KRX 티커, 미국주식은 Yahoo 티커)
ticker_mapping = {
    "영풍": "000670.KQ",
    "롯데손해보험": "000400.KQ",
    "동아에스티": "170900.KQ",
    "노보노디스크": "NVO",
    "아마존": "AMZN"
}

def get_portfolio_message() -> str:
    """
    투자 포트폴리오 메시지 생성
    """
    msg_lines = ["📈 개인 주식 포트폴리오 (실시간 전략 브리핑)", "━━━━━━━━━━━━━━━━━━"]
    
    for name, info in portfolio_data.items():
        ticker = ticker_mapping[name]
        current_price = get_current_price(ticker)
        profit_pct = ((current_price - info["avg_price"]) / info["avg_price"]) * 100
        
        # 전략 판단
        strategy = ""
        if profit_pct >= info["target_profit_pct"]:
            strategy = f"익절 권장 ({info['target_profit_pct']}% 목표 달성) → 일부 익절 후 성장/글로벌 섹터 재투자"
        elif profit_pct <= -info["stop_loss_pct"]:
            strategy = f"손절 최소화 권장 (손실 {info['stop_loss_pct']}% 이상) → 변동성 관찰 후 대응"
        else:
            strategy = "보유 유지 → 섹터 및 글로벌 뉴스 모니터링"

        # 메시지 구성
        line = (
            f"• {name} ({info['issue']})\n"
            f"  - 현재 수익률: {profit_pct:.2f}%\n"
            f"  - 전략: {strategy}\n"
            f"  - 특이 사항: {info['issue']}\n"
            f"  - 리스크 수준: {info['risk_level']}"
        )
        msg_lines.append(line)
    
    msg_lines.append("━━━━━━━━━━━━━━━━━━")
    return "\n".join(msg_lines)
