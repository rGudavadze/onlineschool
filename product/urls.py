from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('product-categories', CategoryViewSet, basename='product-categories')


urlpatterns = [
    url('', include(router.urls))
]
