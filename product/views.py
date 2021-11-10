from rest_framework.response import Response
from rest_framework import viewsets
from .models import Product, Category
from .serializer import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all()
        return products

    def create(self, request, *args, **kwargs):
        data = request.data

        new_product = Product.objects.create(name=data['name'], price=data['price'], available=data['available'],
                                             description=data['description'], slug=data['slug'], quantity=data['quantity'],
                                             category=Category.objects.get(slug=data['category']))

        new_product.save()

        serializer = ProductSerializer(new_product)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        categories = Category.objects.all()
        return categories
