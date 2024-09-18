from django.urls import path
from . import views

app_name = "news"

urlpatterns = [

    path('', views.NewsListView.as_view(), name='news_list'),
    path('create/', views.NewsListView.as_view(), name='news_create'),
    path('<int:pk>/', views.NewsDetailAPIView.as_view(), name='news_detail'),
    path('category/', views.CategoryView.as_view(), name='category_create'),
    path('like/<int:pk>/', views.NewsLikeAPIView.as_view()),
    path('<int:news_pk>/comments/', views.CommentListView.as_view(), name='comment_list'),
    path('comments/<int:comment_pk>/', views.CommentDetailAPIView.as_view(), name='comment_detail'),
    path('user/liked/', views.UserLikedNewsAPIView.as_view()),
    path('news_crawling/', views.WebCrawlingAPIView.as_view(), name='news_crawling'),
]