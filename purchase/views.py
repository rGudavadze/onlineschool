from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAuthenticatedOrReadOnly
from .serializers import PurchaseSerializer
from .models import Purchase, Product


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def list(self, request, *args, **kwargs):
        purchase_list = Purchase.objects.filter(user=request.user)
        serializer = PurchaseSerializer(purchase_list, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        item = Product.objects.get(id=data['product'])

        if request.user.purchase.filter(product=item).first():
            return Response({"message": "You already own this product"})

        new_purchase = Purchase.objects.create(user=request.user, product=item)

        serializer = PurchaseSerializer(new_purchase)

        # if not serializer.is_valid():
        #     return Response({"message": "enter valid data"})

        new_purchase.save()

        return Response(serializer.data)
