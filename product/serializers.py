from rest_framework import serializers
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

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance
