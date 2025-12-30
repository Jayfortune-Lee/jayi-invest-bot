# Market Jayi Bot (자동차/AS + 주식)
from openai import OpenAI
from core.macro import auto_as_macro_prompt
from core.portfolio import analyze_portfolio
from core.telegram_sender import send_message
from core.config import OPENAI_API_KEY, TG_TOKEN_MARKET, TG_ID

client = OpenAI(api_key=OPENAI_API_KEY)

def run_market_bot():
    # 1. 자동차/AS 시장 브리핑
    auto_prompt = auto_as_macro_prompt()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": auto_prompt},
            {"role": "user", "content": "오늘 글로벌 자동차/AS 시장 요약 브리핑해줘"}
        ]
    )
    auto_as_report = response.choices[0].message.content

    # 2. 주식 포트폴리오 브리핑
    stock_report = analyze_portfolio()

    # 3. 최종 메시지 통합
    final_report = f"""
📅 오늘의 전략 브리핑
━━━━━━━━━━━━━━━━━━
🚗 글로벌 자동차/AS 시장
{auto_as_report}

━━━━━━━━━━━━━━━━━━
📈 개인 주식 포트폴리오
{stock_report}
"""
    # 4. Telegram 발송
    send_message(TG_TOKEN_MARKET, TG_ID, final_report)
    print("Market Jayi Bot 메시지 발송 완료")

if __name__ == "__main__":
    run_market_bot()
