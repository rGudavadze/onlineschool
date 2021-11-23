from rest_framework import serializers
from user.models import User
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'slug',
                  'created', 'category', 'seller', 'rating', 'rating_quantity')

    # def validate(self, attrs):
    #     pass
    #
    # def create(self, validated_data):
    #     category_id = validated_data.pop('category', None)
    #     instance = self.Meta.model(category_id=category_id, **validated_data)
    #     instance.save()
    #
    #     return instance
