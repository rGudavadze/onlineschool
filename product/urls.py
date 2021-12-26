from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, SearchView, TopTenProduct


router = DefaultRouter()
router.register('', ProductViewSet, basename='products')


urlpatterns = [
    url('', include(router.urls)),
    path('search/', SearchView.as_view()),
    path('top10product/', TopTenProduct.as_view()),
    path('<product_pk>/reviews/', include('review.urls')),
]
