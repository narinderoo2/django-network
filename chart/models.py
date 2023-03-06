from django.utils import timezone
from django.db import models


class DeviceDetails(models.Model):
    name = models.CharField(max_length=200)
    total_ram = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class ChartDetails(models.Model):
    name = models.ForeignKey(DeviceDetails, on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now_add=True,blank=True,editable=False )
    ram = models.CharField(max_length=200)
    battery = models.CharField(max_length=200)
    cpu = models.CharField(max_length=200)
    modified = models.DateTimeField(blank=True,default=timezone.now())


    def __str__(self):
        return self.ram + " use in your device" 
