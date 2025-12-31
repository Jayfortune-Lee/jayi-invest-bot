import openai
import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def fetch_global_car_as_news():
    """
    실제 뉴스 API 또는 RSS Feed 활용 가능
    간단 예시로 링크 포함
    """
    # 예시 뉴스 링크
    news_links = [
        "https://www.autonews.com",
        "https://www.reuters.com/business/autos-transportation",
        "https://www.marklines.com/en/statistics"
    ]
    
    prompt = (
        "글로벌 자동차/AS 시장 동향을 분석하되, "
        "각 지역별 정치·외교 리스크, 전쟁/재난/파업 등 공급망 교란, "
        "OEM 생산과 AS 부품 수익성 시사점을 포함하고, "
        "주요 뉴스 링크도 같이 제공하라. 최신 데이터 기반."
    )
    
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5
    )
    analysis = response['choices'][0]['message']['content']
    return f"{analysis}\n\n뉴스 링크:\n" + "\n".join(news_links)
