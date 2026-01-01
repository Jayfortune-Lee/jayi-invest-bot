import asyncio
from playwright.async_api import async_playwright

async def get_seoul_auction_items():
    """
    Playwright을 사용하여 실제 경매 정보 사이트에서 
    서울 아파트/유찰/15억 이하 매물을 긁어옵니다.
    """
    items = []
    async with async_playwright() as p:
        # 브라우저 실행
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 보안이 비교적 유연한 무료 경매 정보 페이지
        url = "https://www.dooinauction.com/auction/search/list.php?s_u_p_addr1=서울&s_u_p_target=아파트&s_u_p_status=유찰"
        
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_selector(".list_table", timeout=10000)
            
            rows = await page.query_selector_all(".list_table tr")
            
            # 상위 5개 매물 파싱
            for row in rows[1:6]:
                try:
                    case_no = await (await row.query_selector(".case_no")).inner_text()
                    address = await (await row.query_selector(".address")).inner_text()
                    price_text = await (await row.query_selector(".price")).inner_text()
                    
                    # 가격 전처리 (예: "1,250,000,000원" -> 1250000000)
                    appraisal_value = int(price_text.split('\n')[0].replace(",", "").replace("원", "").strip())
                    
                    if appraisal_value <= 1500000000:
                        items.append({
                            "district": "서울",
                            "case_no": case_no.strip(),
                            "title": address.strip().split('\n')[0],
                            "appraisal_value": appraisal_value,
                            "min_bid_price": int(appraisal_value * 0.8),
                            "status": "유찰"
                        })
                except:
                    continue
        except Exception as e:
            print(f"크롤링 중 에러: {e}")
            
        await browser.close()
    return items
