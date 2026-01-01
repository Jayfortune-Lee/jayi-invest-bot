import os
import asyncio
import datetime
from core.crawler import get_seoul_auction_items
from core.analyzer import ask_gpt
from telegram import Bot
from telegram.request import HTTPXRequest

async def main():
    # 1. 크롤러 데이터 가져오기
    auction_items = get_seoul_auction_items()
    
    # 텔레그램 설정 (타임아웃 방지 및 인스턴스 생성)
    t_request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"), request=t_request)
    chat_id = os.getenv("TG_ID")

    # 매물이 없을 경우 알림
    if not auction_items:
        await bot.send_message(
            chat_id=chat_id, 
            text="📢 **Auction Jayi 알림**\n\n현재 조건(15억 이하)에 맞는 신규 유찰 매물이 없습니다. 내일 다시 확인하겠습니다!"
        )
        return

    # 2. 메시지 구성
    analysis_input = ""
    link_section = "📌 **실시간 경매 상세 정보 확인**\n\n"

    for item in auction_items:
        # 네이버 대신 사용할 대체 사이트 링크 (검색 파라미터 활용)
        # 옥션원(구 굿옥션) 검색 결과 페이지
        auction1_url = f"https://www.auction1.co.kr/auction/search/list.php?search_text={item['case_no']}"
        # 두인옥션 (무료 가입 시 상세 열람 가능)
        dooin_url = f"https://www.dooinauction.com/auction/search/list.php?search_text={item['case_no']}"
        # 공식 법원경매 정보 메인
        court_url = "https://www.courtauction.go.kr/"

        analysis_input += (
            f"📍 [{item['district']}] {item['title']}\n"
            f"- 사건번호: {item['case_no']}\n"
            f"- 금액: 감정 {item['appraisal_value']:,.0f} / 최저 {item['min_bid_price']:,.0f}\n"
            f"- 상태: {item['status']}\n\n"
        )
        
        link_section += (
            f"🏠 **{item['title']}**\n"
            f"👉 [옥션원에서 확인]({auction1_url})\n"
            f"👉 [두인옥션에서 확인]({dooin_url})\n"
            f"🏛️ [대한민국 법원경매 공식홈]({court_url})\n\n"
        )

    # 3. GPT 전문가 분석
    role = "당신은 15억 이하 서울 핵심지 아파트 전문 경매 컨설턴트입니다. 냉철하게 안전마진을 계산합니다."
    
    prompt = f"""
    [오늘의 경매 매물 리스트]
    {analysis_input}
    
    위 매물들을 분석하여 다음 내용을 포함한 리포트를 작성하세요:
    1. 각 매물의 입지적 장점과 실거주 vs 투자 가치 판단.
    2. 최저가 입찰 시 예상되는 시세 차익(안전마진).
    3. '네이버 경매 서비스 종료로 인해 위 대체 링크를 통해 상세 정보를 확인하라'는 안내 멘트 포함.
    """
    
    analysis_result = ask_gpt(prompt, system_role=role)
    
    # 4. 최종 메시지 전송
    final_message = f"🏠 **Auction Jayi: 실전 룰링**\n\n{analysis_result}\n\n{link_section}"
    
    try:
        await bot.send_message(
            chat_id=chat_id, 
            text=final_message, 
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    except Exception:
        # 마크다운 문법 충돌 시 일반 텍스트로 재시도
        clean_message = final_message.replace("*", "").replace("#", "")
        await bot.send_message(chat_id=chat_id, text=clean_message)

if __name__ == "__main__":
    asyncio.run(main())
