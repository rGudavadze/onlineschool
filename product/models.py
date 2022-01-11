from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from user.models import User


def validate_gte_null(value):
    if value < 0:
        raise ValidationError(f"{value} is not a positive number")


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0, validators=[validate_gte_null])
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0, validators=[validate_gte_null, MaxValueValidator(5)])
    rating_quantity = models.IntegerField(default=0, validators=[validate_gte_null])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name
