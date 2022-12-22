from .models import *
from rest_framework import serializers


class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = CountryName
        fields = "__all__"

class StateSerializers(serializers.ModelSerializer):
    country = serializers.CharField(source="countryId.name")
    class Meta:
        model = StateName
        fields = "__all__"

class CitySerializers(serializers.ModelSerializer):
    country = serializers.CharField(source="country.name")
    state = serializers.CharField(source="state.name")

    class Meta:
        model = CityName
        fields = "__all__"

class CountryCreateSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length = 200)
    class Meta:
        model = CountryName
        fields = ("name",)
    
    def validate_name(self,value):
        if CountryName.objects.filter(name=value.upper()).exists():
            raise serializers.ValidationError("Country name is allready exist")
        return value.upper()

class StateCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = StateName
        fields = ("name","countryId")

    def validate_name(self,value):
        if StateName.objects.filter(name=value).exists():
            raise serializers.ValidationError("State name is allready exist")
        return value


class CityCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CityName
        fields = ("name","country","state","latitude","longitude")

   
class StateSerializers(serializers.ModelSerializer):
    class Meta:
        model = StateName
        fields = ('id','name','countryId')

