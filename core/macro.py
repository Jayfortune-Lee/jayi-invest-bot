import openai
import os
import requests
from bs4 import BeautifulSoup

openai.api_key = os.environ.get("OPENAI_API_KEY")

def auto_as_macro_prompt():
    """
    글로벌 자동차/AS 시장 뉴스 + 정치/재난/전쟁/공급망 교란 포함
    """
    # 예시: Yahoo Finance, Google News 등에서 기사 스크래핑
    news_urls = [
        "https://finance.yahoo.com/topic/automotive",
        "https://www.reuters.com/business/autos/"
    ]
    headlines = []
    for url in news_urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.select("h3"):
            text = item.get_text(strip=True)
            if text:
                headlines.append(text)
        if len(headlines) > 10:
            break
    
    prompt = f"다음 글로벌 자동차/AS 관련 뉴스 내용을 전문 투자자 시각으로 요약해줘, 정치·재난·전쟁·공급망 영향 포함:\n{headlines[:10]}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return "🚗 글로벌 자동차/AS 시장\n" + response.choices[0].message.content
