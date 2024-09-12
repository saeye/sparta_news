from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import News, Category
from .serializers import NewsSerializer, CategorySerializer, NewsDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# 카테고리 생성 admin user만 카테고리 생성가능


class CategoryView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

# GET = 목록조회, POST = 게시글 작성


class NewsListView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # 로그인 없이 조회가능, 게시글 작성시 로그인 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    

# 뉴스 게시글 좋아요
class NewsLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        user = request.user

        if news.likes.filter(pk=user.pk).exists():
            news.likes.remove(user)
            message = "좋아요 취소😢"

        else:
            news.likes.add(user)
            message = "좋아요👍"
        
        return Response(data={"message": message}, status=status.HTTP_200_OK)