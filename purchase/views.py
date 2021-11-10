from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import PurchaseSerializer
from .models import Purchase, User, Product
from .permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthenticated)
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        print(type(request.user))

        if request.user.is_anonymous:
            raise AuthenticationFailed("you are not authenticated!")

        item = Product.objects.get(id=data['product'])

        if request.user.purchase.filter(product=item).first():
            return Response({"message": "You already own this product"})

        new_purchase = Purchase.objects.create(user=request.user, product=item)

        serializer = PurchaseSerializer(new_purchase)

        # if not serializer.is_valid():
        #     return Response({"message": "enter valid data"})

        new_purchase.save()

        item.quantity -= 1
        item.save()

        return Response(serializer.data)
