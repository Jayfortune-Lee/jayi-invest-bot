import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_global_car_as_news():
    # 예시: Reuters 글로벌 자동차 뉴스 스크래핑
    url = "https://www.reuters.com/business/autos-transportation/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    headlines = [a.get_text() for a in soup.select("h3 a")][:5]
    news_text = "\n".join([f"- {h}" for h in headlines])
    
    prompt = (
        f"다음 뉴스 기반으로 글로벌 자동차 및 AS 부품 시장 동향을 "
        f"국제 정치/재난/전쟁/공급망 리스크 중심으로 요약하고, "
        f"AS 운영 담당자가 참고할 행동 가이드까지 포함해서 정리해줘.\n\n뉴스:\n{news_text}"
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional financial and automotive market analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
