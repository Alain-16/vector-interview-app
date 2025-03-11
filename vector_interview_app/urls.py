from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import UserSignUpView, UserLoginView,home

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/',home,name='home'),
]