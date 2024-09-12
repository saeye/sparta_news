from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .validators import validate_user_data # validators.py에서 가져오기
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from.serializers import ChangePasswordSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives


# class check_mail(APIView):
#     def get(self, request, email):
        




class UserCreateView(APIView):
    def post(self, request):
        result_msg = validate_user_data(request.data)
        if result_msg:
            return Response({"message": result_msg}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=request.data.get("username"),
            password=request.data.get("password"),
            email=request.data.get("email"),
            is_active=False, # 비활성화, 메일 확인시 활성화
        )
        message = """
            <p>환영합니다. Sparta News에 가입하셨습니다.</p>
            <p>아래 링크를 클릭하여 메일 인증을 완료하세요.</p>
            <a href="{% url 'accounts:email_confirmation' %}">Email confirm</a>
            """
        mail = EmailMultiAlternatives(
            'Sparta News Email confirmation',
            '',
            'commentsofnews@naver.com',
            ['jms070300@naver.com'],# 테스트를 위해 메일 고정함, 실제로는 'jms070300@naver.com'->user.email로 바꿔야함
        )
        mail.attach_alternative(message, "text/html")
        mail.send()
        # send_mail(
        #     'Sparta News Email confirmation',
        #     ,
        #     'commentsofnews@naver.com',  # 발신자 이메일
        #     ["jms070300@naver.com"],  # 수신자 이메일
        #     fail_silently=False,
        #     )
        serializer = UserSerializer(user)
        return Response({"message": "가입 완료👌", "data": serializer.data}, status=status.HTTP_201_CREATED)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필 수정👌"}, serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            old_password = serializer.validated_data("old_password")
            new_password = serializer.validated_data("new_password")
            
            # 현재 비밀번호 맞는지 확인
            if not user.check_password(old_password):
                return Response({"message": "현재 비밀번호가 맞지 않습니다🥺"}, status=status.HTTP_400_BAD_REQUEST)
            
            # 비밀번호 변경
            user.set_password(new_password)
            user.save()

            return Response({"message": "비밀번호 변경 완료👌"}, status=status.HTTP_200_OK)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        user = request.user
        logout(request)
        user.delete()
        return Response({"message": "회원탈퇴 완료👌"}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowView(APIView):
    def post(self, request, user_id):
        current_user = request.user
        target_user = User.objects.get(pk=user_id)

        if current_user.id == target_user.id:
            return Response({"message": "자신을 팔로우할 수 없어요"}, status=status.HTTP_400_BAD_REQUEST)

        elif target_user in current_user.following.all():
            current_user.following.remove(target_user)
            return Response({"message": "팔로우 취소"}, status=status.HTTP_200_OK)
        else:
            current_user.following.add(target_user)
            return Response({"message": "팔로우"}, status=status.HTTP_200_OK)
        
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        following = user.following.all()
        followers = user.followers.all()
        following_count = user.following.count()
        followers_count = user.followers.count()
        ret = {
            'following': following,
            'followers': followers,
            'following_count': following_count,
            'followers_count': followers_count,
        }
        return Response(ret, status=status.HTTP_200_OK)
    
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