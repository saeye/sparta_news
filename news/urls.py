from django.urls import path
from .views import NewsListView, CommentListView, CommentDetailAPIView
app_name = "news"
urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:news_pk>/comments/', CommentListView.as_view(), name='comment_list'),
    path('comments/<int:comment_pk>/', CommentDetailAPIView.as_view(), name='comment_detail'),
]
