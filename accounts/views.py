from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .validators import validate_user_data # validators.py에서 가져오기
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserCreateView(APIView):
    def post(self, request):
        result_msg = validate_user_data(request.data)
        if result_msg:
            return Response({"message": result_msg}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=request.data.get("username"),
            password=request.data.get("password"),
            email=request.data.get("email")
        )
        
        serializer = UserSerializer(user)
        return Response({"message": "가입 완료👌", "data": serializer.data}, status=status.HTTP_201_CREATED)

    
# 로그인
class SigninView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Username or password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 인증 후 토큰 발급
        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)


# 로그아웃
class SignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token_str = request.data.get("refresh_token")
        refresh_token = RefreshToken(refresh_token_str)

        try:
            refresh_token.check_blacklist()
        except Exception:
            return Response({"error": "The token is invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token.blacklist()
        return Response({"message": "You have been logged out."}, status=status.HTTP_200_OK)