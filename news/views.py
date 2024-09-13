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


    # 크롤링한 기사 데이터로 뉴스 작성
class NewsCreateAPIView(CreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # 크롤링하여 데이터 받아왔다고 가정
        article_data = [
            {
                "title": "Mistral releases Pixtral 12B, its first multimodal model",
                "content": "French AI startup Mistral has unveiled its first model capable of processing both images and text. Named Pixtral 12B, this model boasts 12 billion parameters and is approximately 24GB in size. In general, a model’s performance improves with the number of parameters, which are indicative of its problem-solving abilities.\n\nPixtral 12B builds on Mistral’s previous text model, Nemo 12B, and can handle questions about an arbitrary number of images, whether they are provided via URLs or encoded in base64. It shares capabilities with other multimodal models like Anthropic’s Claude family and OpenAI’s GPT-4o, including image captioning and object counting.\n\nThe model is available for download via a torrent link on GitHub and on the AI and machine learning platform Hugging Face, and can be used under an Apache 2.0 license, which imposes no restrictions. This was confirmed by a Mistral spokesperson via email.\n\nUnfortunately, at the time of publication, there were no functioning web demos available to test Pixtral 12B. According to Sophia Yang, head of Mistral developer relations, the model will soon be accessible for testing through Mistral’s chatbot and API platforms, Le Chat and Le Plateforme.\n\nDetails about the image data used to train Pixtral 12B are not clear. Like many generative AI models, it is likely that Pixtral 12B was trained on a large amount of public data from the web, which can often be copyrighted. Although some model developers claim that scraping public data falls under 'fair use,' this practice has been challenged by copyright holders, leading to lawsuits against major companies like OpenAI and Midjourney.",
                # "category": "APPs"
            },
            {
                "title": "",
                "content": "Single people looking to find their soulmates online have traditionally relied on two main methods: trying their luck with dating apps or expanding their social networks on social media to find potential partners. However, some have discovered a third option, using services like Goodreads and Strava to meet others with shared interests and aspirations. These hobby-based apps, which focus on activities like running, reading, or movie-watching, are becoming increasingly popular—not only for dating but for building connections more broadly.\n\nThis trend reflects a shift away from the 'digital town square' provided by platforms like Twitter/X and other social media sites. As dissatisfaction grows with platforms like Twitter, partly due to concerns over free speech and the amplification of hate, alternative apps such as Bluesky and Threads are gaining traction. Users are looking for spaces that connect them based on shared interests rather than algorithm-driven content.\n\nStrava, for instance, has seen a 20% increase in users over the past year, leading to the addition of a messaging feature to complement its workout documentation. Ravelry, a knitting social network, boasts over 9 million users, while Goodreads has amassed more than 150 million members. Letterboxd, an app for film enthusiasts to track, review, and rate movies, has grown from 1.8 million users in March 2020 to over 14 million this summer, reflecting a 55% increase in its monthly active user base.\n\nJess Maddox from the University of Alabama points out that major platforms like Twitter/X, YouTube, TikTok, and Instagram often push algorithmically curated feeds that can limit exposure to desired content. In contrast, hobby apps offer a more focused and less contentious environment. According to Dr. Carolina Are from the Centre for Digital Citizens at Northumbria University, these apps promote connection through shared interests, leading to less need for extensive content moderation and creating a more enjoyable user experience.\n\nLetterboxd, for example, fosters a single-channel conversation where comments are in-line, reducing the potential for public shaming and performative reposting. Similar dynamics exist on Goodreads and Strava, where communication and messaging are possible but public shaming is less likely. The pleasant atmosphere of hobby apps encourages users to spend more time on them, potentially leading to romantic connections as a natural outcome of shared interests. Dating on these platforms can be seen as less pressured and more casual compared to traditional dating apps, which often feel like a 'dating supermarket.'",
                "category": "AI"
            }
        ]

        # 여러 기사 정보를 리스트 형태로 받아올 경우
        # 크롤링한 데이터가 리스트인지 확인
        if isinstance(article_data, list):
            news_objects = []
            for article in article_data:
                title = article.get('title')
                content = article.get('content')
                category_name = article.get('category', 'General')

                # 카테고리 지정 (해당 카테고리 없으면 생성하여 지정)
                category, _ = Category.objects.get_or_create(name=category_name)

                # ChatGPT로 기사내용 번역 or 요약
                try:
                    content = translate_or_summarize(content)
                except Exception as e:
                    return Response({"error": f"ChatGPT 요청 실패: {str(e)}"}, status=500)

                # 기사제목 한국어 번역 / 제목이 없을 경우 기사 내용을 바탕으로 제목을 생성
                try:
                    title = generate_title(content)
                except Exception as e:
                    return Response({"error": f"ChatGPT 요청 실패: {str(e)}"}, status=500)

                serializer = NewsSerializer(data={
                    'title': title,
                    'content': content,
                    'category_id': category.id
                })

                if serializer.is_valid(raise_exception=True):
                    news = serializer.save(author=request.user)
                    news_objects.append(news)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(NewsSerializer(news_objects, many=True).data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)



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
