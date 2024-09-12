from rest_framework import serializers
from .models import News, Comment, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', required=False)
    
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'image', 'category', 'category_id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('news', 'author')
        
    
    # API 응답 커스터마이즈
    def to_representation(self, instance):
        # super: serializers.ModelSerializer
        ret = super().to_representation(instance)
        ret.pop("news")
        return ret
        

class NewsDetailSerializer(NewsSerializer):
    pass
