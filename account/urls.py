from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from .views import *
from .customeToken import CustomTokenObtainPairSerializer


urlpatterns = [
    path('user/', UserProfileView.as_view()),
    path('user-login/',jwt_views.TokenObtainPairView.as_view(
        serializer_class=CustomTokenObtainPairSerializer) ,name='token_obtain_pair'),
    path('email-check/', EmailCheck.as_view()),
    path('forget-password/', OTPCheck.as_view()),

    path('role/', RoleCRUD.as_view()),
    path('role/<int:pk>/', RoleCRUD.as_view()),
    path('permission/', PermissionCRUD.as_view()),
    path('permission/<int:pk>/', PermissionCRUD.as_view()),

    path('user-pagination/', UserPaginationOrder.as_view()),
    path('permission-pagination/', PermissionPaginationOrder.as_view()),

]


