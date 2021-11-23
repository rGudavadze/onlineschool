from django.db import models
from user.models import SellerProfile, User


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    available = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    rating_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
