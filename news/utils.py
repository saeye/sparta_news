from .bots import ask_chatgpt

prompt1 = '''
사용자가 입력한 기사가 한국어로 작성되어있다면 요약해서 기사내용을 작성해주세요. 
기사가 영어로 작성되어있다면, 한국어로 번역해서 기사 내용을 작성해주세요.

본문은 다음 형식으로 작성해 주세요:
중요 부분은 볼드체로 강조합니다.
필요하다면 글머리 기호(예: •)나 볼드체를 활용하여 시각적으로 구분합니다.
전체적으로 깔끔하고 읽기 쉽게 작성해 주세요.
'''

prompt2 = '''
사용자가 입력한 기사의 핵심 내용을 반영하여 한국어로 기사 제목을 작성합니다.
'''

# ChatGPT로 기사내용 번역 or 요약
def translate_or_summarize(content):
    return ask_chatgpt(content, prompt1)

# 제목이 없을 경우 기사 내용을 바탕으로 제목을 생성
def generate_title(content):
    return ask_chatgpt(content, prompt2)