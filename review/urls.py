from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewset


router = DefaultRouter()
router.register('reviews', ReviewViewset, basename='reviews')


urlpatterns = [
  url('', include(router.urls))
]
