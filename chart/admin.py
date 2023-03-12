from django.contrib import admin
from .models import *

admin.site.register(DeviceDetails)


class ChartDetailsAdmin(admin.ModelAdmin):  
    list_display = ('time',)


admin.site.register(ChartDetails,ChartDetailsAdmin)