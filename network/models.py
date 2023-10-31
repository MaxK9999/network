from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes = models.ManyToManyField('Post', related_name="liking_users", blank=True)
    comments = models.ManyToManyField('Comment', related_name="commented_by", blank=True)
    posts = models.ManyToManyField('Post', related_name="posted_by")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)    
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="post_comments", blank=True, null=True)
    
    def __str__(self):
        return f'Comment by {self.user.username} on post {self.post.id}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    body = models.TextField(max_length=500, blank=False)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    comments = models.ManyToManyField(Comment, related_name="post_comments", blank=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "body": self.body,
            "image": self.image,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liked_by": [user.username for user in self.liked_by.all()],
            "comments": [comment.serialize() for comment in self.comments.all()],
        }