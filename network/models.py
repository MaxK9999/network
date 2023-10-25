from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)    


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    body = models.TextField(max_length=500, blank=False)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True, null=True)
    comments = models.ManyToManyField(Comment, related_name="post_comments", blank=True, null=True)
    
    def __str__(self):
        return f"Post {self.id} made by {self.user}"
    
    