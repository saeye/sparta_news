from django.db import models
from django.conf import settings
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')
    # category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True) # 카테고리
    
    def __str__(self):
        return self.title