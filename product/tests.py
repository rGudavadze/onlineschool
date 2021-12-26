from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product
from user.models import User


class ProductTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Category.objects.create(name='test_category')
        User.objects.create_user(
            name="test",
            username="test",
            email="test@gmail.com",
            password="test123@",
            role="USER"
        )
        User.objects.create_user(
            name="test_seller",
            username="test_seller",
            email="test_seller@gmail.com",
            password="test123@",
            role="SELLER"
        )

    def test_create_product(self):
        token = self.client.post('/api/v1/user/login/', {
            'username': 'test_seller',
            'password': 'test123@'
        }).data['jwt']

        response = self.client.post('/api/v1/products/products/', data={
            "name": "test_product",
            "price": 100,
            "description": "this is description about test product",
            "category": 1
        }, HTTP_AUTHORIZATION=f'Bearer {token}', format='json')

        self.assertEqual(response.status_code, 201)

    def test_create_product_with_user(self):
        token = self.client.post('/api/v1/user/login/', {
            'username': 'test',
            'password': 'test123@'
        }).data['jwt']

        response = self.client.post('/api/v1/products/products/', data={
            "name": "test_product",
            "price": 100,
            "description": "this is description about test product",
            "category": 1
        }, HTTP_AUTHORIZATION=f'Bearer {token}', format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message'), "You do not have permission to add course!")

    def test_update_product(self):
        product = Product.objects.create(name="test_product",
                                         price=100,
                                         description="this is description about test product",
                                         category=Category.objects.get(name="test_category"))
        token = self.client.post('/api/v1/user/login/', {
            'username': 'test_seller',
            'password': 'test123@'
        }).data['jwt']

        response = self.client.patch(f'/api/v1/products/products/{product.id}/', data={
            "price": 50
        }, HTTP_AUTHORIZATION=f'Bearer {token}', format='json')

        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        product = Product.objects.create(name="test_product",
                                         price=100,
                                         description="this is description about test product",
                                         category=Category.objects.get(name="test_category"))
        token = self.client.post('/api/v1/user/login/', {
            'username': 'test_seller',
            'password': 'test123@'
        }).data['jwt']

        response = self.client.delete(f'/api/v1/products/products/{product.id}/',
                                      HTTP_AUTHORIZATION=f'Bearer {token}', format='json')

        self.assertEqual(response.status_code, 204)
