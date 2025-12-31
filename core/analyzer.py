import openai
import os

def ask_gpt(prompt):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "당신은 자동차 산업 전문가이자 자산운용가, 경매 컨설턴트입니다."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
