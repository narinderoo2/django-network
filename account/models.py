from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from os.path import splitext



class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=30, blank=True)
    phone_number=models.CharField(blank=True,max_length=20,null=True)
    flag=models.CharField(default='in',max_length=10)
    user_timezone = models.CharField(max_length=250, null=True, blank=True, default="Asia/Kolkata")
    create_at = models.DateField(auto_now=True)
    password_attempted = models.CharField(default=0,max_length=2)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    
    def __str__(self):
        return self.email

def image_upload_to(instance, filename):
    now = timezone.now()
    base, extension = splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"profileImage/{base}_{now:%Y%m%d%H%M%S}{milliseconds}{extension}"
   
DefaultImage = 'profileImage/default.png'



class ProfileImage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to, default=DefaultImage)