from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        following = User.following.all()
        followers = User.followers.all()
        following_count = serializers.IntegerField(source="following.count", read_only=True)
        followers_count = serializers.IntegerField(source="followers.count", read_only=True)