import requests

TARGET_DISTRICTS = ["강남구","서초구","동작구","용산구","송파구","성동구","광진구"]

def fetch_auction_listings():
    """
    가상의 API 예시
    실제로는 법원경매, 부동산 공공 API 연동
    """
    listings = []
    for district in TARGET_DISTRICTS:
        # 예시 데이터
        listings.append({
            "district": district,
            "apt_name": f"{district} 아파트 예시",
            "size": 84,
            "price": 12_500_000_000,
            "link": "https://example.com/auction",
            "rights_issue": "명도권 문제 없음",
            "safety": "상대적 안전"
        })
    return listings

def generate_auction_brief():
    listings = fetch_auction_listings()
    summary = ""
    for apt in listings:
        bid_price = int(apt["price"] * 0.88)
        summary += (f"{apt['district']} {apt['apt_name']} ({apt['size']}㎡) "
                    f"권리분석: {apt['rights_issue']}, "
                    f"안전성: {apt['safety']}, "
                    f"예상 입찰가: {bid_price:,}원\n"
                    f"링크: {apt['link']}\n\n")
    return summary
