from django.urls import path
from .views import NewsListView, NewsDetailAPIView, CategoryView
app_name = "news"
urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailAPIView.as_view(), name='news_detail'),
    path('category/', CategoryView.as_view(), name='category_create'),
]
