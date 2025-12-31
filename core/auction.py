import requests
from bs4 import BeautifulSoup

def fetch_seoul_auction():
    url = "https://www.courtauction.go.kr/common/bidder/auctionList.do"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    
    # 실제로는 태그 구조 확인 후 필터링
    apartments = []
    for item in soup.select(".auction-item"):
        name = item.select_one(".apt-name").text
        size = float(item.select_one(".apt-size").text.replace("㎡",""))
        price = int(item.select_one(".current-price").text.replace(",",""))
        rights = item.select_one(".rights-info").text
        if size >= 84 and price <= 1500000000:
            apartments.append({"address": name, "current_price": price, "rights_issues": rights})
    return apartments

def analyze_auction(apartment):
    suggested_bid = apartment["current_price"] * 0.88
    safety_note = "상대적으로 안전" if "권리분석 문제 없음" in apartment["rights_issues"] else "리스크 있음"
    return f"{apartment['address']} | 권리분석: {apartment['rights_issues']} | 추천입찰가: {suggested_bid:,.0f}원 | {safety_note}"
