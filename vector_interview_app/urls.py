from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import UserSignUpView, UserLoginView,home,InterviewController

interview_list = InterviewController.as_view({
    'get':'list',
    'post':'create'
})

interview_detail = InterviewController.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy'
})

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/',home,name='home'),
    path('interview/',interview_list, name='create-interview'),
    path('interview/<int:pk>/',interview_detail,name='interview-record'),
]