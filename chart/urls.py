from django.urls import path
from .views import*




urlpatterns = [
    path('test/', TestingCPU.as_view(),name="testView"),
]