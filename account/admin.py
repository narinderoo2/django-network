from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(ProfileImage)
admin.site.register(OtpConfirm)
admin.site.register(PasswordHistory)
