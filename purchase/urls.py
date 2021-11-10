from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet


router = DefaultRouter()
router.register('purchase', PurchaseViewSet, basename='purchase')


urlpatterns = [
    url('', include(router.urls))
]
