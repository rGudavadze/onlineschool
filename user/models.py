from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=256)
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    password_confirm = models.CharField(max_length=256)
    role = models.CharField(max_length=9, choices=(("USER", "user"), ("SELLER", "seller")), default="USER")

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Profile(models.Model):
    cash = models.FloatField(max_length=256, default=0)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s profile"


class SellerProfile(models.Model):
    user = models.OneToOneField(User, related_name='seller_profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s profile (seller)"
