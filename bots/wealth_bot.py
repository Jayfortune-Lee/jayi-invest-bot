import os
import asyncio
import yfinance as yf
from core.google_sheet import get_portfolio_data
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    portfolio = get_portfolio_data()
    # (앞선 정량 데이터 계산 로직 동일...)
    summary = "종목별 수익률 및 손익 데이터..." # 예시

    # 오직 수익만 보는 투자 전문가 역할 부여
    role = "당신은 냉혹한 월스트리트 투자자입니다. 오직 수익률 극대화와 기회비용만을 따져서 행동 지침을 내립니다."
    
    prompt = f"아래 포트폴리오를 보고 돈을 더 벌기 위해 '매도/보유/추매'를 단호하게 결정하세요.\n{summary}"
    
    analysis = ask_gpt(prompt, system_role=role)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"))
    await bot.send_message(chat_id=os.getenv("TG_ID"), text=f"💰 **Wealth Jayi: 수익 전략**\n\n{analysis}", parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
