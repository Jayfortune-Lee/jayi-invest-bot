import requests

NEWS_API_KEY = "YOUR_NEWSAPI_KEY"  # NewsAPI 무료 키 입력

def get_macro_news(keyword, limit=1):
    url = f"https://newsapi.org/v2/everything?q={keyword}&sortBy=publishedAt&apiKey={NEWS_API_KEY}&pageSize={limit}&language=ko"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    return [(a['title'], a['url']) for a in articles]

def auto_as_macro_prompt():
    regions = ["미국", "중국", "유럽", "중동", "러시아", "멕시코", "동남아시아"]
    prompt = "🚗 글로벌 자동차/AS 시장 브리핑\n━━━━━━━━━━━━━━━━━━\n"

    for r in regions:
        news_list = get_macro_news(f"{r} 자동차 OR AS 부품", limit=1)
        news_str = " | ".join([f"[{t}]({l})" for t, l in news_list]) if news_list else "관련 뉴스 없음"
        prompt += f"- {r}: {news_str}\n"

    prompt += "\n공급망, OEM, AS 수익성 관련 시사점 포함"
    return prompt
