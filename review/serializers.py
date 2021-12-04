from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'rating', 'user', 'product')

    def validate(self, attrs):
        user = attrs.get('user')
        product = attrs.get('product')

        if product.review.filter(user=user).first():
            raise serializers.ValidationError("You already reviewed the product!")

        return super().validate(attrs)

    def create(self, validated_data):
        product = validated_data.get('product')

        instance = self.Meta.model(**validated_data)
        instance.save()

        product.rating = (product.rating * product.rating_quantity + validated_data['rating']) / \
                         (product.rating_quantity + 1)
        product.rating_quantity += 1
        product.save()

        return instance

    def update(self, instance, validated_data):
        pass
