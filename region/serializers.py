from .models import *
from rest_framework import serializers


class CountrySerializers(serializers.ModelSerializer):
    state_count = serializers.SerializerMethodField()

    class Meta:
        model = CountryName
        fields = ("name",'description','state_count','id')
    
    def get_state_count(self, obj):
        ord = StateName.objects.filter(countryId=obj.id).count()
        return ord


class StateSerializers(serializers.ModelSerializer):
    country_name = serializers.CharField(source="countryId.name")
    city_count = serializers.SerializerMethodField()
    class Meta:
        model = StateName
        fields =  ('name','id','countryId','country_name','city_count')


    def get_city_count(self, obj):
        ord = CityName.objects.filter(state=obj.id).count()
        return ord


class CitySerializers(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name")
    state_name = serializers.CharField(source="state.name")

    class Meta:
        model = CityName
        fields = ('name','country','country_name','state_name','state','latitude','longitude','id')





class CountryCreateSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length = 200)
    class Meta:
        model = CountryName
        fields = ("name","description")
    
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

   
