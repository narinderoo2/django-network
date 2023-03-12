
from django.contrib import admin
from django.urls import  include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('region/', include('region.urls')),

path('chart/', include("chart.urls")),    
    # path('socket/', include('websocket.urls')),
]
