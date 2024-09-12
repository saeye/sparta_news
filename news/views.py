from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import News, Category
from .serializers import NewsSerializer, CategorySerializer, NewsDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
# Create your views here.

# 카테고리 생성 admin user만 카테고리 생성가능


class CategoryView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

# GET = 목록조회, POST = 게시글 작성


class NewsListView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # 로그인 없이 조회 가능, 게시글 작성 시 로그인 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = News.objects.all()
        search_title_content_query = self.request.query_params.get('q', None) # 통합 검색 /api/news/?q=제목+내용
        title_query = self.request.query_params.get('title', None)  # 제목만 검색: /api/news/?title=제목
        content_query = self.request.query_params.get('content', None) # 내용만 검색: /api/news/?content=내용
        author_query = self.request.query_params.get('author', None) # 저자만 검색: /api/news/?author=저자
        
        # 제목, 내용 모두 검색
        if search_title_content_query: 
            queryset = queryset.filter(
                Q(title__icontains=search_title_content_query) |
                Q(content__icontains=search_title_content_query)
                )
        # 제목, 내용, 저자 각각 따로 검색
        else: 
            if title_query:
                queryset = queryset.filter(title__icontains=title_query)
            if content_query:
                queryset = queryset.filter(content__icontains=content_query)
            if author_query:
                queryset = queryset.filter(author__username__icontains=author_query)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # 접근 제한
    # 두 번 이상 반복되는 로직은 함수로 빼면 좋습니다👀

    def get_object(self, pk):
        return get_object_or_404(News, pk=pk)

    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsDetailSerializer(news)
        return Response(serializer.data)

    def put(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsDetailSerializer(
            news, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        news = self.get_object(pk)
        news.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)
