from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAuthenticatedOrReadOnly
from .serializers import ReviewSerializer
from .models import Review
from product.models import Product


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    queryset = Review.objects.all()

    # def list(self, request, *args, **kwargs):
    #     reviews_list = Review.objects.filter(user=request.user)
    #     serializer = ReviewSerializer(reviews_list, many=True)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        current_product = Product.objects.get(id=data['product'])

        is_reviewed = current_product.review.filter(user=request.user).first()
        if is_reviewed:
            return Response({"message": "You already reviewed the product!"})

        new_review = Review.objects.create(text=data['text'],
                                           rating=data['rating'],
                                           user=request.user,
                                           product=current_product)

        current_product.rating = (current_product.rating * current_product.rating_quantity + data['rating']) / \
                                 (current_product.rating_quantity + 1)
        current_product.rating_quantity += 1
        current_product.save()

        serializer = ReviewSerializer(new_review)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReviewSerializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        updated_data = request.data
        instance = self.get_object()

        old_rating = instance.rating
        current_product = instance.product

        if "rating" in updated_data:
            current_product.rating = (round(current_product.rating * current_product.rating_quantity) -
                                      old_rating + updated_data['rating']) / \
                                      current_product.rating_quantity
            current_product.save()

        serializer = ReviewSerializer(instance, data=updated_data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        current_product = instance.product

        try:
            current_product.rating = (round(current_product.rating * current_product.rating_quantity) - instance.rating) / \
                                     (current_product.rating_quantity - 1)

            current_product.rating_quantity -= 1

        except ZeroDivisionError:
            current_product.rating = 0
            current_product.rating_quantity = 0

        current_product.save()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
