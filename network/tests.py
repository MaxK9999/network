from django.test import TestCase
from network.models import User, Post, Comment
from django.urls import reverse
import json

# Create your tests here.
class AppTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    
    # Test index view
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        assert response.status_code == 200, f"Status code is {response.status_code}"
        
    
    # Test whether posts can be created
    def test_create_post(self):
        response = self.client.post(
            reverse('new_post'),
            data={
                'body': 'Test post body',
            }
        )
        self.assertEqual(response.status_code, 302)


    # Test whether posts can be liked
    def test_like_and_unlike_post(self):
        # Create a test post
        test_post = Post.objects.create(
            user=self.user, body='Test post body'
        )

        # Like the post
        self.user.liked_posts.add(test_post)
        self.assertEqual(test_post.liked_by.count(), 1)

        # Unlike the post
        self.user.liked_posts.remove(test_post)
        self.assertEqual(test_post.liked_by.count(), 0)
    
    
    # Test whether comments can be created
    def test_create_comment(self):
        # Create test post
        post = Post.objects.create(user=self.user, body='Test post')
        
        # Create test comment
        comment = Comment.objects.create(
            user=self.user, post=post, body='Test comment'
        )
        
        # Check comment creation
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.body, 'Test comment')
        
    
    # Test follow and unfollow
    def test_follow_and_unfollow(self):
        # Create test user
        test_user = User.objects.create_user(username='testuser2', password='testpassword')
        
        # Follow the user
        self.user.followers.add(test_user)
        self.assertEqual(self.user.followers.count(), 1)
        
        # Unfollow the user
        self.user.followers.remove(test_user)
        self.assertEqual(self.user.followers.count(), 0)
