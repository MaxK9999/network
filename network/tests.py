from django.test import TestCase
from network.models import User

# Create your tests here.
class AppTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        
    def test_index_view(self):
        response = self.client.get('network/index.html')
        self.assertEqual(response.status_code, 404)