import asyncio
from playwright.async_api import async_playwright

async def get_realtime_auction_data():
    """
    Playwright을 사용하여 실제 경매 정보 사이트에서 
    서울 아파트/유찰/15억 이하 매물을 긁어옵니다.
    """
    async with async_playwright() as p:
        # 브라우저 실행 (Headless 모드)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 보안이 비교적 유연한 무료 경매 정보 페이지로 접속
        # 예: 두인옥션 검색 결과 페이지 (서울/아파트/유찰)
        url = "https://www.dooinauction.com/auction/search/list.php?s_u_p_addr1=서울&s_u_p_target=아파트&s_u_p_status=유찰"
        await page.goto(url)
        
        # 페이지 로딩 대기
        await page.wait_for_selector(".list_table")
        
        items = []
        # 리스트 테이블의 행(row)들을 가져옴
        rows = await page.query_selector_all(".list_table tr")
        
        for row in rows[1:6]:  # 상위 5개 매물만 테스트
            try:
                # 사건번호 추출
                case_no = await (await row.query_selector(".case_no")).inner_text()
                # 소재지/단지명 추출
                title = await (await row.query_selector(".address")).inner_text()
                # 감정가 추출
                appraisal_text = await (await row.query_selector(".price")).inner_text()
                appraisal_value = int(appraisal_text.replace(",", "").replace("원", ""))
                
                # 15억 이하 필터링
                if appraisal_value <= 1500000000:
                    items.append({
                        "district": "서울",
                        "case_no": case_no.strip(),
                        "title": title.strip().split('\n')[0],
                        "appraisal_value": appraisal_value,
                        "min_bid_price": int(appraisal_value * 0.8), # 유찰 시 통상 20% 저감
                        "status": "유찰 1회"
                    })
            except:
                continue
                
        await browser.close()
        return items

# 기존 동기 함수와 호환을 위한 래퍼
def get_seoul_auction_items():
    return asyncio.run(get_realtime_auction_data())
