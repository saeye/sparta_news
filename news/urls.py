from django.urls import path
from .views import NewsListView, CategoryView
app_name = "news"
urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('category/', CategoryView.as_view(), name='category_create'),
]
