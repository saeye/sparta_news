from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', views.NewsDetailAPIView.as_view(), name='news_detail'),
    path('category/', views.CategoryView.as_view(), name='category_create'),
    path('news/<int:pk>/like/', views.NewsLikeAPIView.as_view()),
]
