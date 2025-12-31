import os
import asyncio
import feedparser # 구글 뉴스를 위해 추가 (pip install feedparser)
from core.analyzer import ask_gpt
from telegram import Bot
from telegram.request import HTTPXRequest

async def main():
    # 1. 구글 뉴스 RSS 활용 (현대차 관련 핵심 키워드)
    # 한글 뉴스도 섞어서 더 풍부하게 가져옵니다.
    rss_urls = [
        "https://news.google.com/rss/search?q=현대자동차+공급망+글로벌&hl=ko&gl=KR&ceid=KR:ko",
        "https://news.google.com/rss/search?q=Hyundai+Motor+Supply+Chain+Strategy&hl=en-US&gl=US&ceid=US:en"
    ]
    
    news_data = ""
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]: # 각 URL당 최신 3개씩
            news_data += f"- {entry.title} (출처: {entry.source.get('title', 'Google News')})\n"

    # 만약 진짜 뉴스가 하나도 없다면 리포트를 중단하거나 경고 메시지 출력
    if not news_data:
        news_data = "현재 현대차 관련 긴급 글로벌 뉴스가 검색되지 않습니다. 최근 환율 및 원자재 동향 위주로 분석 바랍니다."

    # 현대차 재직자 페르소나 (사용자님 직장 고려)
    role = "당신은 현대자동차 글로벌 전략실의 수석 분석가입니다. 동료(재직자)에게 실무적인 통찰력을 제공하는 것이 목표입니다."
    
    prompt = f"""
    [실시간 수집 뉴스 리스트]
    {news_data}
    
    [분석 요청]
    1. 위 뉴스들이 현대차의 글로벌 생산 및 AS 공급망에 미칠 '진짜' 영향을 실무자 관점에서 분석하세요.
    2. 절대 가상의 시나리오를 쓰지 마세요. 뉴스 내용이 부족하면 현재 자동차 산업의 3대 리스크(전기차 캐즘, 공급망 다변화, 환율)를 바탕으로 현대차에 적용하세요.
    3. '가상의 시나리오'라는 말은 절대 언급하지 마세요.
    """
    
    report = ask_gpt(prompt, system_role=role)

    # 텔레그램 타임아웃 방지
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"), request=t_request)
    
    await bot.send_message(
        chat_id=os.getenv("TG_ID"), 
        text=f"🚙 **Hyundai Jayi: 실무 브리핑**\n\n{report}", 
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    asyncio.run(main())
