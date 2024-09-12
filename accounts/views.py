from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .validators import validate_user_data  # validators.py에서 가져오기 by saeye

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