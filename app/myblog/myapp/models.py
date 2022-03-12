from django.db import models

class Post(models.Model):
    title = models.CharField('title', max_length=50)
    content = models.TextField('content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    