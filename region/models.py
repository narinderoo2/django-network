from django.db import models

class CountryName(models.Model):
    name = models.CharField(max_length=200 , unique=True)
    description = models.CharField(max_length=250, blank=True,null=True)
    created_by = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name 

class StateName(models.Model):
    name= models.CharField(max_length=200,unique=True)
    countryId = models.ForeignKey(CountryName, on_delete=models.CASCADE,
    related_name='state')   # cascade that only the CASCADE action is not clear.
    
    createdBy = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name + self.countryId.name


class CityName(models.Model):
    country = models.ForeignKey(CountryName, on_delete=models.CASCADE, related_name='country')
    state = models.ForeignKey(StateName,on_delete=models.CASCADE,related_name='state')
    name = models.CharField(max_length=200)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.name + '-'+ self.state.name +'-' +self.country.name
