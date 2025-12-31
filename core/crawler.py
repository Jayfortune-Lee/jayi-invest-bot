def get_seoul_auction_items():
    """
    강남3구, 마용성, 광진, 동작, 강동구 중 감정가 15억 이하 매물만 수집
    """
    # 실제 수집 데이터 예시 (15억 이하 필터링 적용 버전)
    all_items = [
        {
            "district": "송파구",
            "case_no": "2023타경8890",
            "title": "가락동 가락금호 84㎡",
            "appraisal_value": 1450000000, 
            "min_bid_price": 1160000000,
            "status": "유찰 1회",
            "market_price": "실거래 13.8억",
            "description": "가락시장역 더블역세권. 실거주 선호도 높고 리모델링 호재 있음."
        },
        {
            "district": "강동구",
            "case_no": "2024타경1122",
            "title": "고덕동 고덕그라시움 59㎡",
            "appraisal_value": 1300000000, 
            "min_bid_price": 1040000000,
            "status": "유찰 1회",
            "market_price": "급매 12.3억",
            "description": "9호선 연장 호재. 신축 대단지 커뮤니티 최상. 실거주 및 투자 동시 가능."
        },
        {
            "district": "성동구",
            "case_no": "2024타경4455",
            "title": "행당동 대림아파트 59㎡",
            "appraisal_value": 1100000000,
            "min_bid_price": 880000000,
            "status": "유찰 1회",
            "market_price": "실거래 10.5억",
            "description": "5호선 행당역 초역세권. 쿼드러플 역세권 왕십리역 인접. 직주근접 최강."
        },
        {
            "district": "동작구",
            "case_no": "2023타경9988",
            "title": "사당동 사당롯데캐슬골든포레 59㎡",
            "appraisal_value": 1250000000,
            "min_bid_price": 1000000000,
            "status": "유찰 1회",
            "market_price": "매가 11.8억 수준",
            "description": "숲세권 단지. 강남 출퇴근 용이. 신축급 컨디션으로 실거주 만족도 높음."
        },
        {
            "district": "마포구",
            "case_no": "2024타경7766",
            "title": "성산동 성산시영 47㎡",
            "appraisal_value": 1050000000,
            "min_bid_price": 840000000,
            "status": "유찰 1회",
            "market_price": "시세 10억 선",
            "description": "강북 재건축 최대어. 마포구 핵심 투자 종목. 몸테크 및 장기투자 적합."
        }
    ]
    
    # 15억 이하 매물만 필터링하는 Ruling
    budget_limit = 1500000000
    filtered_items = [item for item in all_items if item['appraisal_value'] <= budget_limit]
    
    return filtered_items
