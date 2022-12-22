from django.contrib import admin
from .models import *


class CountryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# admin.site.register(Book, BookAdmin)

admin.site.register(CountryName,CountryAdmin)
admin.site.register(CityName)
admin.site.register(StateName)
