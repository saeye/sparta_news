from django.urls import path
from .views import NewsListView, NewsDetailAPIView
app_name = "news"
urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailAPIView.as_view(), name='news_detail'),
]
