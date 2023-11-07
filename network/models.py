from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(max_length=200, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    likes = models.ManyToManyField('Post', related_name="liking_users", blank=True)
    comments = models.ManyToManyField('Comment', related_name="commented_by", blank=True)
    posts = models.ManyToManyField('Post', related_name="posted_by", blank=True)	
    
    def is_followed_by(self, user):
        return Follower.objects.filter(user_to=self, user_from=user).exists()
    

class Follower(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="relation_from")
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="relation_to")
    created = models.DateTimeField(default=timezone.now, db_index=True)
    
    def __str__(self):
        return f'{self.user_from.username} follows {self.user_to.username}'


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
    
    def formatted_timestamp(self):
        return self.timestamp.astimezone(timezone.get_current_timezone()).strftime("%d-%m-%Y %H:%M:%S")
    def serialize(self):
        
        return { 
            "id": self.id,
            "user": self.user,
            "body": self.body,
            "image": self.image,
            "timestamp": self.formatted_timestamp(),
            "liked_by": [user.username for user in self.liked_by.all()],
            "comments": [comment.serialize() for comment in self.comments.all()],
        }