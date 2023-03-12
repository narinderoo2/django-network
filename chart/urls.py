from django.urls import path
from .views import*




urlpatterns = [
    path('device-details/', PcDeviceDetails.as_view(),name="deviceDetails"),
]