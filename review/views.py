from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer
from .models import Review
from product.models import Product


class ReviewViewset(viewsets.ModelViewSet):
  serializer_class = ReviewSerializer
  permission_classes=(IsAuthenticated,)
  queryset = Review.objects.all()

  def create(self, request, *args, **kwargs):
    data = request.data

    current_product = Product.objects.get(id=data['product'])

    new_review = Review.objects.create(text=data['text'], rating=data['rating'], user=request.user, product=current_product)

    new_review.save()

    serializer = ReviewSerializer(new_review)

    return Response(serializer.data)
