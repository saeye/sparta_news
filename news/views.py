from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import News, Comment, Category
from .serializers import NewsSerializer, CommentSerializer, CategorySerializer, NewsDetailSerializer
from django.core.mail import send_mail
from .utils import translate_or_summarize, generate_title
from bs4 import BeautifulSoup
import requests
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
        search_title_content_query = self.request.query_params.get(
            'q', None)  # 통합 검색 /api/news/?q=제목+내용
        title_query = self.request.query_params.get(
            'title', None)  # 제목만 검색: /api/news/?title=제목
        content_query = self.request.query_params.get(
            'content', None)  # 내용만 검색: /api/news/?content=내용
        author_query = self.request.query_params.get(
            'author', None)  # 저자만 검색: /api/news/?author=저자

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
                queryset = queryset.filter(
                    author__username__icontains=author_query)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        # 포인트 지급
        user = self.request.user
        user.point += 3
        user.save()

        return Response({"message": "글 작성 포인트💰(3) 지급되었습니다."}, status=status.HTTP_201_CREATED)

class WebCrawlingAPIView(APIView):
    permission_classes = [IsAdminUser]  # 관리자만 크롤링을 수행할 수 있게 제한

    def post(self, request):  # POST 요청이 들어오면 크롤링을 수행 & 데이터 저장
        url = request.data.get('url')  # URL을 클라이언트가 제공

        # URL이 제공되지 않았을 경우 에러 처리
        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # URL을 기반으로 어떤 파서 함수를 쓸지 결정
            parser = self.get_news_parser(url)
        except ValueError as e:
            # 지원되지 않는 뉴스 사이트일 때 단순한 오류 메시지를 반환
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 1. 해당 URL에서 크롤링 진행
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 파서를 통해 제목과 내용을 가져옴
            try:
                title, content = parser(soup)

                # 제목이나 내용이 유효하지 않으면 예외 처리
                if not title or not content:
                    raise ValueError("유효한 제목 또는 내용을 찾을 수 없습니다.")
            except Exception as e:
                return Response({"error": f"지원하지 않는 사이트입니다.: {str(e)}"}, status=500)

            # 카테고리는 기본값으로 'General'을 설정하거나 요청으로 받음
            category_name = request.data.get('category', 'General')
            category, _ = Category.objects.get_or_create(name=category_name)

            # 크롤링한 데이터를 번역 또는 요약
            try:
                content = translate_or_summarize(content)
            except Exception as e:
                return Response({"error": f"ChatGPT 요청 실패: {str(e)}"}, status=500)

            # ChatGPT로 기사내용 번역 or 요약
            try:
                title = generate_title(content)
            except Exception as e:
                return Response({"error": f"ChatGPT 요청 실패: {str(e)}"}, status=500)

            # 2. 크롤링한 데이터를 News 모델에 저장
            serializer = NewsSerializer(data={
                'title': title,
                'content': content,
                'category_id': category.id,
            })

            if serializer.is_valid(raise_exception=True):
                news = serializer.save(author=request.user)
                return Response(NewsDetailSerializer(news).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": "Failed to retrieve the webpage"}, status=status.HTTP_400_BAD_REQUEST)

    def get_news_parser(self, url):
        """
        뉴스 사이트에 맞는 파서 함수를 반환하는 메서드
        """
        if 'naver.com' in url:
            return self.parse_naver_news
        elif 'daum.net' in url:
            return self.parse_daum_news
        else:
            return self.else_news

    def parse_naver_news(self, soup):
        """
        네이버 뉴스 파싱
        """
        # h2 태그 내의 span 태그에서 제목 추출
        title_tag = soup.find('h2', class_='media_end_head_headline')
        title = title_tag.find('span').get_text() if title_tag and title_tag.find('span') else None

        # div 태그에서 내용 추출
        content_div = soup.find('div', class_='newsct_article _article_body')
        content = content_div.get_text() if content_div else None

        return title, content

    def parse_daum_news(self, soup):
        """
        다음 뉴스 파싱
        """
        title_tag = soup.find('h3', class_='tit_view')
        title = title_tag.get_text() if title_tag else None

        content_div = soup.find('div', class_='article_view')
        content = content_div.get_text() if content_div else None

        return title, content

    def else_news(self, soup):
        """
        기타 뉴스 파싱
        """
        title_tag = soup.find('h1')
        title = title_tag.get_text() if title_tag else None

        content_div = soup.find('div', class_='article-content')
        content = content_div.get_text() if content_div else None



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

    # 댓글 목록 조회
    def get(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        comments = news.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # 댓글 작성
    def post(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, news=news)


            user = request.user
            user.point += 2
            user.save()
    

            post_author_email = news.author.email
            send_mail(
                '새로운 댓글이 달렸습니다',
                f'{request.user.username}님이 "{news.title}" 게시글에 댓글을 달았습니다.',
                'commentsofnews@naver.com',  # 발신자 이메일
                [post_author_email],  # 수신자 이메일
                fail_silently=False,
            )

            return Response({"message": "댓글 작성 포인트 +2 💰"}, serializer.data, status=status.HTTP_201_CREATED)



class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    # 댓글 삭제
    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
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

            user.point += 1
            user.save()
            return Response({"message": "댓글 작성 완료👌 포인트(1) 지급 완료!💰"}, user.data, status=status.HTTP_201_CREATED)
        

        return Response(data={"message": message}, status=status.HTTP_200_OK)


# 좋아요한 뉴스 조회
class UserLikedNewsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        liked_news = News.objects.filter(likes=user)
        serializer = NewsSerializer(liked_news, many=True)

        return Response(serializer.data)
