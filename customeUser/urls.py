

#  rt@gmail.com
# ccit

    
from django.contrib import admin
from django.urls import  include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('region/', include('region.urls')),
]
