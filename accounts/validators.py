from django.contrib.auth.models import User

def validate_user_data(user_data):
    username = user_data.get("username")
    password = user_data.get("password")
    email = user_data.get("email")

    if User.objects.filter(username=username).exists():
        return "이미 존재하는 username이야🫠"
    
    if User.objects.filter(email=email).exists():
        return "오잉? 이미 존재하는 email이야🫠"
    

    