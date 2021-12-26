from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.role != "SELLER":
            return Response(
                {"message": "You do not have permission to add course!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data
        data['seller'] = user.pk

        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()


class SearchView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        search = request.data.get('search')

        if search:
            result = Product.objects.filter(name__icontains=search)

        else:
            result = Product.objects.all()

        serializer = ProductSerializer(result, many=True)
        return Response(serializer.data)


class TopTenProduct(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by("-rating")[:10]
