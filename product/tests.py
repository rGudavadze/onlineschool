from django.test import TestCase
from .models import Product, Category


class ProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Cat", slug="cat")
        category.save()

        product = Product.objects.create(name='new item', price=500, available=True,
                                         description='this is new item', slug='new-item', quantity=15,
                                         category=category)
        product.save()

    def test_product_content(self):
        product = Product.objects.get(id=1)
        name = f"{product.name}"
        price = f"{product.price}"
        available = f"{product.available}"
        description = f"{product.description}"
        slug = f"{product.slug}"
        quantity = f"{product.quantity}"
        category_name = f"{product.category.name}"
        category_slug = f"{product.category.slug}"

        self.assertEqual(name, 'new item')
        self.assertEqual(price, '500.0')
        self.assertEqual(available, 'True')
        self.assertEqual(description, 'this is new item')
        self.assertEqual(slug, 'new-item')
        self.assertEqual(quantity, '15')
        self.assertEqual(category_name, 'Cat')
        self.assertEqual(category_slug, 'cat')
