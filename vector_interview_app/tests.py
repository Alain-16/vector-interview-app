from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSignupTest(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'test123',
            'password2': 'test123',
        }
    def test_signup_success(self):
        response = self.client.post(self.signup_url,data=self.user_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())
    
    def test_signup_password_missmatch(self):
        invalid_data = self.user_data.copy()
        invalid_data['password'] = "testpassword"
        response = self.client.post(self.signup_url,data=invalid_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password does not match",str(response.data))
    
    def test_login_and_token_obtain(self):
        self.client.post(self.signup_url,data=self.user_data,format='json')
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        }
        response = self.client.post(self.login_url,data=login_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access',response.data)
        self.assertIn('refresh',response.data)
    
    def test_token_refresh(self):
        self.client.post(self.signup_url,data=self.user_data,format='json')
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        }
        login_response = self.client.post(self.login_url,data=login_data,format='json')
        refresh_token = login_response.data.get('refresh')
        response = self.client.post(self.refresh_url,data={'refresh': refresh_token},format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn("access",response.data)