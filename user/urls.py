from django.urls import path
from .views import RegisterView, LoginView, UserView, Logout, ListUser


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserView.as_view()),
    path('logout/', Logout.as_view()),
    path('users/', ListUser.as_view())
]
