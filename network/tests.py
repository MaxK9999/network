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
        response = self.client.get('network/index.html')
        self.assertEqual(response.status_code, 404) # Change this to 200 when index has been completed to actually view it
        
    
    # Test whether posts can be created
    def test_create_post(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'body': 'This is a test post.'
        }
        response = self.client.post(reverse('new_post'), data=json.dumps(data), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
    
    # Test whether comments can be places under a  post
    def test_create_comment(self):
        self.client.login(username='testuser', password='testpassword')
        post = Post.objects.create(user=self.user, body='A test post')
        data = {
            'text': 'This is a test comment.'
        }
        response = self.client.post(reverse('create_comment', kwargs={'post_id': post.id}),
                                    data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)