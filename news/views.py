from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import News, Comment, Category
from .serializers import NewsSerializer, CommentSerializer, CategorySerializer, NewsDetailSerializer


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


"""
글 조회시 댓글을 함께 반환할 경우
class NewsDetailView(RetrieveAPIView):
queryset = News.objects.all()
serializer_class = NewsSerializer

def get(self, request, id):
    news = get_object_or_404(News, id=id)
    comments = news.comments.all()  # 해당 게시글에 달린 모든 댓글 조회
    news_data = NewsSerializer(news).data
    comment_data = CommentSerializer(comments, many=True).data
    response_data = {
        'news': news_data,
        'comments': comment_data
    }
    return Response(response_data)
"""      
class CommentListView(APIView):
    # 인증(로그인)해야 이 기능 사용할 수 있게 함
    permission_classes = [IsAuthenticated]
    
    #댓글 목록 조회
    def get(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        comments = news.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    # 댓글 작성
    def post(self, request, news_pk):
        news=get_object_or_404(News, pk=news_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, news=news)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)
    
    # 댓글 삭제
    def delete(self,request, comment_pk):
        comment= self.get_object(comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # 댓글 수정
    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


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