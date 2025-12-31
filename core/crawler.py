import requests
from bs4 import BeautifulSoup

def get_seoul_auction_items():
    """
    네이버 경매 시황 등을 참고하여 분석 대상 매물 리스트를 생성합니다.
    (실제 복잡한 크롤링 차단을 피하기 위해 핵심 매물 정보 구조를 생성하는 함수)
    """
    # 실제 구현 시에는 특정 경매 정보 API나 웹 페이지를 파싱합니다.
    # 여기서는 GPT가 분석하기 가장 좋은 형태의 '실시간급' 데이터 구조를 반환합니다.
    
    items = [
        {
            "case_no": "2023타경112456",
            "title": "강남구 대치동 한보미도맨션 84㎡",
            "appraisal_value": 2800000000,
            "min_bid_price": 2240000000,
            "status": "유찰 1회",
            "market_price": "실거래 27억 선",
            "description": "양재천 인근, 대치동 학원가 인접. 재건축 초기 단계로 대지지분 높음."
        },
        {
            "case_no": "2024타경3345",
            "title": "성동구 옥수동 래미안옥수리버젠 59㎡",
            "appraisal_value": 1600000000,
            "min_bid_price": 1280000000,
            "status": "유찰 1회",
            "market_price": "매가 15.5억 수준",
            "description": "한강진입 용이, 고지대이나 커뮤니티 우수. 강남 접근성 최상."
        },
        {
            "case_no": "2023타경7890",
            "title": "도봉구 창동 주공 3단지 41㎡",
            "appraisal_value": 550000000,
            "min_bid_price": 352000000,
            "status": "유찰 2회",
            "market_price": "급매 4.8억",
            "description": "GTX-C 창동역 호재. 소액 투자 및 갭투자 수요 높음."
        }
    ]
    return items
