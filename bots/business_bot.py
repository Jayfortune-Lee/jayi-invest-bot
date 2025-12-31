import os
import asyncio
import feedparser
from core.analyzer import ask_gpt
from telegram import Bot
from telegram.request import HTTPXRequest

async def main():
    # 1. 구글 뉴스 RSS 활용 (현대차 전략 키워드)
    rss_urls = [
        "https://news.google.com/rss/search?q=현대자동차+공급망+전략&hl=ko&gl=KR&ceid=KR:ko",
        "https://news.google.com/rss/search?q=Hyundai+Motor+Global+Supply+Chain&hl=en-US&gl=US&ceid=US:en"
    ]
    
    news_contents = "" # GPT 분석용
    source_links = "🔗 **분석 근거 뉴스 원문**\n" # 사용자 확인용
    
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]: # 각 검색어당 최신 3개
            news_contents += f"- 제목: {entry.title}\n"
            source_links += f"👉 [{entry.title}]({entry.link})\n"

    if not news_contents:
        news_contents = "최근 24시간 내 현대차 관련 긴급 뉴스가 없습니다. 일반적인 업황 리스크로 분석하세요."
        source_links += "최근 업데이트된 뉴스가 없습니다."

    # 2. GPT 전문가 페르소나 및 분석 요청
    role = "당신은 현대자동차 글로벌 전략실 수석 분석가입니다. 재직자인 동료에게 실무 지침을 전달하세요."
    
    prompt = f"""
    [실시간 뉴스 데이터]
    {news_contents}
    
    위 뉴스를 바탕으로 현대차 생산/AS 공급망에 미칠 영향을 분석하세요. 
    전문 용어를 적절히 섞어 실무 리포트 형식으로 작성하되, 분석 끝에 '상세 내용은 아래 링크를 참조하라'고 멘트하세요.
    """
    
    report = ask_gpt(prompt, system_role=role)

    # 3. 텔레그램 전송 설정
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    bot = Bot(token=os.getenv("TG_TOKEN_MARKET"), request=t_request)
    
    # 분석 리포트 + 뉴스 링크 결합
    final_message = f"🚙 **Hyundai Jayi: 실무 브리핑**\n\n{report}\n\n---\n{source_links}"
    
    try:
        await bot.send_message(
            chat_id=os.getenv("TG_ID"), 
            text=final_message, 
            parse_mode="Markdown",
            disable_web_page_preview=True # 링크 미리보기로 메시지가 너무 길어지는 것 방지
        )
    except Exception as e:
        # 마크다운 특수문자 에러 대비 일반 텍스트 전송
        await bot.send_message(chat_id=os.getenv("TG_ID"), text=final_message.replace("*", ""))

if __name__ == "__main__":
    asyncio.run(main())
