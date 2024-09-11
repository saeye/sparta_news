from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import News
from .serializers import NewsSerializer, NewsDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

# GET = 목록조회, POST = 게시글 작성
class NewsListView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 로그인 없이 조회가능, 게시글 작성시 로그인 필수
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsDetailAPIView(APIView):
    permission_classes = [AllowAny]  # 접근 제한
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