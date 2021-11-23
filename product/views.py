from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.is_anonymous or user.role != "SELLER":
            return Response(
                {"message": "You do not have permission to add course!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data

        new_product = Product.objects.create(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            seller=user,
            category=Category.objects.get(slug=data['category'])
        )

        serializer = ProductSerializer(new_product)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        categories = Category.objects.all()
        return categories
