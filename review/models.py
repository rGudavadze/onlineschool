from django.db import models
from user.models import User
from product.models import Product


class Review(models.Model):
    CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='review', on_delete=models.CASCADE)

    def __str__(self):
        return f"Review from {self.user.name} on {self.product.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"], name="unique_review_user_product"
            )
        ]
