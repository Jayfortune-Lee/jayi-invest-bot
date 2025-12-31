import requests
import pandas as pd
from bs4 import BeautifulSoup

# 관심 지역과 조건
TARGET_GU = ["강남구","서초구","동작구","용산구","송파구","성동구","광진구"]
MIN_AREA = 84         # 84㎡ 이상
MAX_PRICE = 15_000_000_000  # 15억 이하

def fetch_auction_list():
    """
    공공 경매 API 또는 웹사이트에서 서울 아파트 경매 물건을 가져오는 예시.
    여기서는 웹 스크래핑 형태로 구현 (예시 URL, 실제 API 교체 필요)
    """
    url = "https://example-auction-site.com/seoul-apartment"  # 실제 API/웹 교체 필요
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 테이블/리스트 구조에 맞게 parsing (예시)
    data = []
    rows = soup.select("table.auction-list tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        gu = cols[1].text.strip()
        area = float(cols[2].text.strip().replace("㎡",""))
        price = int(cols[3].text.strip().replace(",",""))
        link = cols[4].find("a")["href"]
        if gu in TARGET_GU and area >= MIN_AREA and price <= MAX_PRICE:
            data.append({
                "gu": gu,
                "area": area,
                "price": price,
                "link": link
            })
    return data

def analyze_rights(auction):
    """
    간단한 권리분석
    예시: 근저당, 가압류, 임차인, 토지 공유자 수 등
    """
    # 실제는 경매 사이트에서 상세페이지 크롤링 필요
    auction["rights_issue"] = "근저당 1건, 가압류 0건, 임차인 있음"
    
    # 추천 입찰가: 현재 시세 대비 85~90% 수준
    auction["recommended_bid"] = int(auction["price"] * 0.88)
    return auction

def get_auction_message():
    auctions = fetch_auction_list()
    if not auctions:
        return "📢 오늘 조건에 맞는 경매 아파트 매물 없음."

    lines = ["🏢 오늘 서울 경매 아파트 매물 브리핑\n━━━━━━━━━━━━━━━━━━"]
    for a in auctions:
        a = analyze_rights(a)
        line = f"• {a['gu']} {a['area']}㎡ / 감정가: {a['price']:,}원\n  권리분석: {a['rights_issue']}\n  추천 입찰가: {a['recommended_bid']:,}원\n  [상세보기]({a['link']})"
        lines.append(line)
    return "\n".join(lines)
