from .models import User

def validate_user_data(user_data):
    username = user_data.get("username")
    password = user_data.get("password")
    email = user_data.get("email")

    if User.objects.filter(username=username).exists():
        return "이미 존재하는 username이에요🫠"
    
    if User.objects.filter(email=email).exists():
        return "이미 존재하는 email이에요"

    if len(password) < 8:
        return "비밀번호는 8자 이상이어야 해요🫠"
    return None
    