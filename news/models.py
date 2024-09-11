from django.db import models
from django.conf import settings
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True) # 카테고리는 게시글과 1:N 관계, 빈칸 허용, null 허용, 카테고리가 삭제될 경우 각 게시글의 해당 카테고리는 null 처리됨
    
    def __str__(self):
        return self.title