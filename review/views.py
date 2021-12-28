from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ReviewSerializer
from .models import Review
from product.models import Product


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = Review.objects.all()

    @staticmethod
    def rating_update_after_delete_product(review, product):
        try:
            product.rating = (int(product.rating * product.rating_quantity + 0.5)
                              - review.rating) / \
                             (product.rating_quantity - 1)

            product.rating_quantity -= 1

        except ZeroDivisionError:
            product.rating = 0
            product.rating_quantity = 0

        product.save()

    def list(self, request, *args, **kwargs):
        product_id = kwargs.get('product_pk')
        if not product_id:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product = Product.objects.filter(pk=product_id).first()
        reviews_list = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews_list, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['product'] = kwargs.get('product_id')
        data['user'] = request.user.id

        serializer = ReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        updated_data = request.data
        updated_data['product'] = kwargs.get('product_id')

        instance = self.get_object()

        serializer = ReviewSerializer(instance, data=updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        current_product = instance.product

        ReviewViewSet.rating_update_after_delete_product(instance, current_product)

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
