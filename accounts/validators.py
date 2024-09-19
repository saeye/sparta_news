from .models import User
import re

def validate_user_data(user_data):
    username = user_data.get("username")
    password = user_data.get("password")
    email = user_data.get("email")

    if User.objects.filter(username=username).exists():
        return "이미 존재하는 username이에요🫠"
    elif username is None:
        return "username을 입력하세요"
    
    if User.objects.filter(email=email).exists():
        return "이미 존재하는 email이에요"
    elif email is None:
        return "email을 입력하세요"
    elif "@" not in email:
        return "email 형식에 맞춰주세요."
        
    elif email.split("@")[1] not in email_list:
        email_list = ["naver.com", "gmail.com", "daum.net"]
        return f"허용되지 않은 email 주소입니다.\n{email_list} 중 하나만 입력하세요"
    
    if len(password) < 8:
        return "비밀번호는 8자 이상이어야 해요🫠"
    elif password in None:
        return "비밀번호를 입력하세요"
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


