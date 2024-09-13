from .models import User

def validate_user_data(user_data):
    username = user_data.get("username")
    password = user_data.get("password")
    email = user_data.get("email")

    if User.objects.filter(username=username).exists():
        return "이미 존재하는 username이에요🫠"
    
    if User.objects.filter(email=email).exists():
        return "이미 존재하는 email이에요"
    if "@" not in email:
        return "email 형식에 맞춰주세요."
    email_list = ["naver.com", "gmail.com", "daum.net"]
    if email.split("@")[1] not in email_list:
        return f"허용되지 않은 email 주소입니다.\n{email_list} 중 하나만 입력하세요"
    
    if len(password) < 8:
        return "비밀번호는 8자 이상이어야 해요🫠"
    return None
    