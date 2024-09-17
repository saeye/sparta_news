from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]

class UserupdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    point = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ["email", "intro", "profile_image", "username", "point"]

    def validate_password(self, value):
        if value == self.instance.password:
            return serializers.ValidationError("변경할 비번호가 원래 비번호와 동일함🤔")
        return value
    
    def validate_email(self, value):
        user = self.instance

        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            return serializers.ValidationError("이미 존재하는 이메일입니다✋")
        return value
    
class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        return value
    