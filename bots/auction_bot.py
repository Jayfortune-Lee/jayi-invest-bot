import os
import asyncio
from core.crawler import get_seoul_auction_items
from core.analyzer import ask_gpt
from telegram import Bot

async def main():
    # 1. 크롤러에서 핵심 지역 매물 가져오기
    auction_items = get_seoul_auction_items()
    
    if not auction_items:
        print("분석할 신규 매물이 없습니다.")
        return

    # 2. GPT 분석용 텍스트와 텔레그램 출력용 텍스트 분리
    analysis_input = ""
    link_section = "📌 **실제 매물 검토 링크 (클릭 시 이동)**\n\n"

    for item in auction_items:
        # 네이버 경매 검색 결과 링크 생성
        search_url = f"https://land.naver.com/auction/search.naver?query={item['case_no']}"
        
        # GPT에게 줄 상세 정보
        analysis_input += (
            f"📍 [{item['district']}] {item['title']}\n"
            f"- 사건번호: {item['case_no']}\n"
            f"- 가격: 감정 {item['appraisal_value']:,.0f} / 최저 {item['min_bid_price']:,.0f}\n"
            f"- 시세/특징: {item['market_price']} / {item['description']}\n\n"
        )
        
        # 사용자에게 보여줄 직접 링크 섹션
        link_section += (
            f"🏠 **{item['title']}**\n"
            f"👉 [사진 및 권리분석 확인하기]({search_url})\n\n"
        )

    # 3. GPT 분석 (투자 전문가 페르소나)
    role = "당신은 수익률에 미친 실전 경매 고수입니다. 분석 시 반드시 [투자용/실거주용]을 구분하고 '돈이 안 되면 하지 마라'고 직설적으로 말합니다."
    
    prompt = f"""
    아래 서울 핵심지 경매 리스트를 분석하라:
    {analysis_input}
    
    분석 가이드라인:
    1. 각 매물에 [투자용] 또는 [실거주용] 딱지를 붙일 것.
    2. '시세 - 낙찰가 - 세금'을 고려해 예상 수익금을 숫자로 때려줄 것.
    3. 네이버 링크를 눌러서 상세 정보를 확인하라고 사용자에게 권유할 것.
    """
    
    analysis_result = ask_gpt(prompt, system_role=role)
    
    # 4. 최종 메시지 결합 및 전송
    final_message = f"🏠 **Auction Jayi: 실전 경매 룰링**\n\n{analysis_result}\n\n{link_section}"
    
    bot = Bot(token=os.getenv("TG_TOKEN_AUCTION"))
    
    # 메시지가 길 경우를 대비해 분할 전송 로직 포함
    try:
        await bot.send_message(
            chat_id=os.getenv("TG_ID"), 
            text=final_message, 
            parse_mode="Markdown",
            disable_web_page_preview=False # 링크 미리보기 활성화
        )
    except Exception as e:
        # Markdown 에러 방지용 일반 텍스트 전송
        await bot.send_message(chat_id=os.getenv("TG_ID"), text=final_message.replace("*", ""))

if __name__ == "__main__":
    asyncio.run(main())
