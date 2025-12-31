# ... (상단 생략) ...
async def main():
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    auction_items = get_seoul_auction_items()
    
    # ... (중략) ...

    prompt = f"""
    오늘 날짜: {today_str}
    분석 대상 매물:
    {analysis_input}
    
    [지시사항]
    1. 너는 오늘 아침 막 올라온 경매 공고를 분석하는 전문가다. 
    2. 과거 자료는 무시하고, 현재 시세와 금리 상황을 반영하여 [투자용/실거주용]을 분류하라.
    3. 사건번호가 {today_str} 기준 유효한지 판단하고 분석하라.
    """
    # ... (하단 생략) ...
