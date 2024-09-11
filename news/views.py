from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import News, Category
from .serializers import NewsSerializer, CategorySerializer
# Create your views here.

#카테고리 생성 admin user만 카테고리 생성가능
class CategoryView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

# GET = 목록조회, POST = 게시글 작성
class NewsListView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 로그인 없이 조회가능, 게시글 작성시 로그인 필수
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)