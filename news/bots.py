import openai
from django.conf import settings

openai.api_key = settings.OPEN_API_KEY

def ask_chatgpt(user_message, system_instructions):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ],
    )
    
    # 응답에서 메시지 추출
    try:
        return completion.choices[0].message['content']
    except (KeyError, IndexError):
        return "ChatGPT 응답 처리 오류: {e}"