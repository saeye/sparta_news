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
        fields = ['id', 'content', 'created_at', 'updated_at', 'author']
        