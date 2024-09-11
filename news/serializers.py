from rest_framework import serializers
from .models import News, Comment


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('news',)
        
    
    # API 응답 커스터마이즈
    def to_representation(self, instance):
        # super: serializers.ModelSerializer
        ret = super().to_representation(instance)
        ret.pop("article")
        return ret
        