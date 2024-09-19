from .models import User
import re

def validate_user_data(user_data):
    # 필수 입력 값 확인
    required_fields = ['username', 'password', 'email']
    missing_fields = [field for field in required_fields if not user_data.get(field)]

    # 누락된 필드가 있을 경우 각 필드에 맞는 메시지 반환
    if missing_fields:
        return f"{', '.join(missing_fields)}를(을) 입력하세요."

    username = user_data.get("username")
    password = user_data.get("password")
    email = user_data.get("email")

    email_list = ["naver.com", "gmail.com", "daum.net"]

    # username 중복 확인
    if User.objects.filter(username=username).exists():
        return "이미 존재하는 username이에요🫠"
    
    # email 중복 및 형식 확인
    if User.objects.filter(email=email).exists():
        return "이미 존재하는 email이에요"
    elif "@" not in email:
        return "email 형식에 맞춰주세요."
    elif email.split("@")[1] not in email_list:
        return f"허용되지 않은 email 주소입니다.\n{email_list} 중 하나만 입력하세요"
    
    # 비밀번호 길이 및 형식 확인
    if len(password) < 8:
        return "비밀번호는 8자 이상이어야 해요🫠"
    
    return None


def changepasswordValidation(pwd):

    if len(pwd) < 8:
    # 비밀번호는 최소 8자 이상이어야 함
        return False
        
    elif re.search('[0-9]+', pwd) is None:
        # 비밀번호는 최소 1개 이상의 숫자가 포함되어야 함
        return False
        
    elif re.search('[a-zA-Z]+', pwd) is None:
        # 비밀번호는 최소 1개 이상의 영문 대소문자가 포함되어야 함
        return False
        
    elif re.search('[`~!@#$%^&*(),<.>/?]+', pwd) is None:
        # 비밀번호는 최소 1개 이상의 특수문자가 포함되어야 함
        return False
        
    else:
        return True


