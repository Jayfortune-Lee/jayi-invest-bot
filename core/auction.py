import requests
from bs4 import BeautifulSoup

# 관심 지역과 조건
TARGET_GU = ["강남구","서초구","동작구","용산구","송파구","성동구","광진구"]
MIN_AREA = 84         # 84㎡ 이상
MAX_PRICE = 15_000_000_000  # 15억 이하

def fetch_auction_list():
    """
    공공 경매 API 또는 웹사이트에서 서울 아파트 경매 물건을 가져오는 예시.
    """
    url = "https://example-auction-site.com/seoul-apartment"  # 실제 API/웹 교체 필요
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
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
    권리분석 기반 추천 입찰가 및 상대적 안전도 계산
    """
    # --- 예시 권리분석 ---
    rights = {
        "mortgage": 1,       # 근저당
        "attachments": 0,    # 가압류
        "tenant": True       # 임차인 여부
    }
    auction["rights_issue"] = f"근저당 {rights['mortgage']}건, 가압류 {rights['attachments']}건, 임차인 있음" if rights["tenant"] else "없음"

    # --- 추천 입찰가 계산 ---
    if rights["mortgage"] > 2 or rights["attachments"] > 1:
        base_rate = 0.85  # 위험 높음
        safety = "⚠️ 위험"
    elif rights["mortgage"] > 0 or rights["attachments"] > 0 or rights["tenant"]:
        base_rate = 0.88  # 약간 위험
        safety = "⚠️ 보통"
    else:
        base_rate = 0.90  # 안정적
        safety = "✅ 상대적으로 안전"

    auction["recommended_bid"] = int(auction["price"] * base_rate)
    auction["safety"] = safety
    return auction

def get_auction_message():
    auctions = fetch_auction_list()
    if not auctions:
        return "📢 오늘 조건에 맞는 경매 아파트 매물 없음."

    lines = ["🏢 오늘 서울 경매 아파트 매물 브리핑\n━━━━━━━━━━━━━━━━━━"]
    for a in auctions:
        a = analyze_rights(a)
        line = f"• {a['gu']} {a['area']}㎡ / 감정가: {a['price']:,}원\n  권리분석: {a['rights_issue']}\n  추천 입찰가: {a['recommended_bid']:,}원\n  안전도: {a['safety']}\n  [상세보기]({a['link']})"
        lines.append(line)
    return "\n".join(lines)
