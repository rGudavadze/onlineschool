from django.db import models
from user.models import User
from product.models import Product


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='review', on_delete=models.CASCADE)

    def __str__(self):
        return f"Review from {self.user.name} on {self.product.name}"

    class Meta:
        ordering = ("-created",)
        # unique_together = ""
