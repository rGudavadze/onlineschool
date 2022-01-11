from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'rating', 'created', 'user', 'product')

    @staticmethod
    def rating_update_after_create_review(product, validated_data):
        product.rating = (product.rating * product.rating_quantity + validated_data['rating']) / \
                         (product.rating_quantity + 1)
        product.rating_quantity += 1
        product.save()

    @staticmethod
    def rating_update_after_update_review(product, old_rating, updated_data):
        product.rating = (int(product.rating * product.rating_quantity + 0.5) -
                          old_rating + updated_data['rating']) / product.rating_quantity

        product.save()

    def create(self, validated_data):
        instance = super().create(validated_data)

        product = validated_data.get('product')
        ReviewSerializer.rating_update_after_create_review(product, validated_data)

        return instance

    def update(self, instance, validated_data):
        validated_data.pop('product')

        old_rating = instance.rating
        current_product = instance.product

        instance = super().update(instance, validated_data)

        if "rating" in validated_data:
            ReviewSerializer.rating_update_after_update_review(current_product, old_rating, validated_data)

        return instance
