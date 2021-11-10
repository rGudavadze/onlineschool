from django.db import models
from user.models import User
from product.models import Product


class Purchase(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='purchase', default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='purchase', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} purchased {self.product.name} that costs ${self.product.price}"
