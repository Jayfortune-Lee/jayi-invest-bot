import openai
import os

def ask_gpt(prompt):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # 시스템 프롬프트에 '현대자동차 재직자'임을 명시
    system_message = """
    당신은 현대자동차(Hyundai Motors)의 글로벌 AS 및 공급망 전략 전문가입니다.
    사용자는 현대자동차에 재직 중이며, 글로벌 자동차 시장의 리스크를 관리합니다.
    모든 분석은 현대자동차의 시장 점유율, 생산 라인(HMI, HMMA 등), 부품 수급(현대모비스 등)의 관점에서 작성하세요.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
