from .models import User

def validate_user_data(user_data):
    username = user_data.get("username")
    password = user_data.get("password")

    if not username:
        return "유저네임을 입력해주세요👀"

    if not password:
        return "비밀번호를 입력해주세요👀"

    if User.objects.filter(username=username).exists():
        return "이미 존재하는 username이에요🫠"

    if len(password) < 8:
        return "비밀번호는 8자 이상이어야 해요🫠"

    return None
