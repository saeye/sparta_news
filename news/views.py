from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
# Create your views here.

# GET = 목록조회, POST = 게시글 작성
class NewsListView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 로그인 없이 조회가능, 게시글 작성시 로그인 필수
    
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
    