from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    url('', include(router.urls))
]
