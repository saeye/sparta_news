from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import News
from .serializers import NewsSerializer
# Create your views here.

# GET = 목록조회, POST = 게시글 작성
class NewsListView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 로그인 없이 조회가능, 게시글 작성시 로그인 필수
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)