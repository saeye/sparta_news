from rest_framework import serializers
from .models import News, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')
    
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'image']


class NewsDetailSerializer(NewsSerializer):
    pass