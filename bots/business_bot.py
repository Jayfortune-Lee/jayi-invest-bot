import os
import asyncio
import yfinance as yf
from core.analyzer import ask_gpt
from telegram import Bot
from telegram.request import HTTPXRequest # 타임아웃 설정을 위해 추가

async def main():
    search_keywords = ["Hyundai Motor Global News", "Automotive Supply Chain Crisis", "Hyundai Competitor BYD Tesla"]
    news_data = ""
    try:
        for kw in search_keywords:
            search = yf.Search(kw, max_results=2)
            for news in search.news:
                news_data += f"- {news['title']}\n"
    except:
        news_data = "최신 뉴스를 가져오는 중 일부 오류가 발생했습니다."

    # 현대차 재직자 전용 역할 부여
    role = "당신은 현대자동차의 글로벌 공급망 및 AS 전략 전문가입니다. 사용자는 현대차 재직자입니다."
    
    prompt = f"""
    [현대차 재직자용 긴급 브리핑]
    최근 뉴스: {news_data}
    
    현대자동차의 입장에서 위 뉴스가 미칠 영향과 대응책을 분석하세요. 
    전문 용어를 사용해도 좋으니 실무에 도움이 되게 작성하세요.
    """
    
    report = ask_gpt(prompt, system_role=role)

    # 텔레그램 타임아웃 설정 (네트워크 지연 방지)
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"), request=t_request)
    
    try:
        await bot.send_message(
            chat_id=os.getenv("TG_ID"), 
            text=f"🚙 **Hyundai Jayi: 업무 리포트**\n\n{report}", 
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"전송 실패, 일반 텍스트로 재시도: {e}")
        # 마크다운 특수문자 충돌 가능성 대비 일반 텍스트 전송
        await bot.send_message(
            chat_id=os.getenv("TG_ID"), 
            text=f"🚙 [Hyundai Jayi 리포트]\n\n{report}"
        )

if __name__ == "__main__":
    asyncio.run(main())
