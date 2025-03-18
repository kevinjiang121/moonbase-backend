from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from apps.users.models import User

class SignupTests(APITestCase):
    def test_signup_success(self):
        url = reverse('signup')
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        user = User.objects.get(username="testuser")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(check_password("password123", user.password_hash))
        self.assertEqual(response.data.get("username"), "testuser")
        self.assertEqual(response.data.get("email"), "testuser@example.com")
        self.assertNotIn("password", response.data)

    def test_signup_invalid_data(self):
        url = reverse('signup')
        data = {
            "username": "",
            "email": "invalid_email",
            "password": "short"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            password_hash=make_password("password123")
        )

    def test_login_success(self):
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertEqual(response.data.get("user")["username"], "testuser")

    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access_token", response.data)
