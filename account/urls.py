from django.urls import path
from .views import *

urlpatterns = [
    # path('', views.index, name='index'),
    path('user/', UserProfileView.as_view()),
    path('user-create/', UserProfileView.as_view()),
    path('user-pagination/', UserPaginationOrder.as_view()),


]