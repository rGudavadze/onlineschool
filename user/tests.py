from django.test import TestCase
from rest_framework.test import APIClient
from .models import User


class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.old_user = User.objects.create_user(
            name="old",
            username="old",
            email="old@gmail.com",
            password="old123@",
            role="USER"
        )

    def test_register_user(self):
        response = self.client.post('/api/v1/user/register/', {
            "name": "test",
            "username": "test",
            "email": "test@gmail.com",
            "password": "test123@",
            "password_confirm": "test123@",
            "role": "USER"
        })

        self.assertEqual(response.status_code, 200)

    def test_register_seller(self):
        response = self.client.post('/api/v1/user/register/', {
            "name": "test",
            "username": "test",
            "email": "test@gmail.com",
            "password": "test123@",
            "password_confirm": "test123@",
            "role": "SELLER"
        })

        self.assertEqual(response.status_code, 200)

    def test_register_user_passwords_not_match(self):
        response = self.client.post('/api/v1/user/register/', {
            "name": "test",
            "username": "test",
            "email": "test@gmail.com",
            "password": "test123@",
            "password_confirm": "test123@@@@@",
            "role": "USER"
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('non_field_errors')[0], 'Passwords are not matched!')


class LoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            name="test",
            username="test",
            email="test@gmail.com",
            password="test123@",
            role="USER"
        )

    def test_login(self):
        response = self.client.post('/api/v1/user/login/', {
            'username': 'test',
            'password': 'test123@'
        })

        self.assertEqual(response.status_code, 200)

    def test_login_wrong_username(self):
        response = self.client.post('/api/v1/user/login/', {
            'username': 'test11111',
            'password': 'test123@'
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_wrong_password(self):
        response = self.client.post('/api/v1/user/login/', {
            'username': 'test',
            'password': 'test123@@@@@'
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Invalid credentials')


class UserViewTest(TestCase):
    def setUp(self):
        self.factory = APIClient()

        self.user = User.objects.create_user(
            name="test",
            username="test",
            email="test@gmail.com",
            password="test123@",
            role="USER"
        )

        self.token = self.client.post('/api/v1/user/login/', {
            'username': 'test',
            'password': 'test123@'
        }).data['jwt']

    def test_get_user(self):
        response = self.client.get('/api/v1/user/profile/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.token}',
                                   format='json')

        self.assertEqual(response.status_code, 200)
