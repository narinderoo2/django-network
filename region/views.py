from django.shortcuts import render
from .models import *
from .serializers import *
from commonutils.pagination import GenericPagiantion

from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter,SearchFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CountryChanges(APIView):

    def post(self,request):
        '''
                if country_ser.is_valid(raise_exception=True):
                    serializers error message show
        '''
        country_ser = CountryCreateSerializers(data=request.data)
        if country_ser.is_valid():
            country_ser.save()
            rsp = {
                'resCode':'1',
                'message':'Country create succesfully'
            }
            return Response(rsp,status=status.HTTP_200_OK)
        rsp = {
            'resCode':'0',
            "message":"Sorry, country name is already exist",
            "serializerError":country_ser.errors,
    
    }
        return Response(rsp,status=status.HTTP_200_OK)


    def delete(self,request,pk=None):
        if pk is not None:
            try:
                check_id = CountryName.objects.get(pk=pk)
            except CountryName.DoesNotExist:
                rsp = {
                    "resCode":'0',
                    'message':'Please select correct country name ',
                }
                return Response(rsp,status=status.HTTP_200_OK)
            else:
                check_id.delete()
                rsp = {'rspCode':'1','message':'Country has been deleted succesfully'}    
        else:
            rsp = {
            'resCode':'0',
            "message":"Sorry, Country name is not valid",
        }
        return Response(rsp,status=status.HTTP_200_OK)

    def get(self,request,pk=None):
        country_data = CountryName.objects.all()
        serializer = CountrySerializers(country_data,many=True)
        rep = {'resCode':'1','result':serializer.data}
        return Response(rep,status=status.HTTP_200_OK)

class StateChanges(APIView):

    def post(self,request):
        '''
                if state_ser.is_valid(raise_exception=True):
                    serializers error message show
        '''
        state_ser = StateCreateSerializers(data=request.data)

        print(state_ser,'--->')
        if state_ser.is_valid():

            
            state_ser.save()
            rsp = {
                'resCode':'1',
                'message':'State create succesfully'
            }
            return Response(rsp,status=status.HTTP_200_OK)
        rsp = {
            'resCode':'0',
            "message":"Sorry, State name is already exist",
            "serializerError":state_ser.errors,
        }
        return Response(rsp,status=status.HTTP_200_OK)

    def patch(self,request,pk=None):
        if pk is not None:
            try:
                get_id = StateName.objects.get(pk=pk)
            except StateName.DoesNotExist:
                rsp={
                "resCode":'0',
                'message':'Select state name is not valid'}
                return Response(rsp,status=status.HTTP_200_OK)
            else:
                state_ser = StateCreateSerializers(get_id,data=request.data,partial=True)
                if state_ser.is_valid():
                    state_ser.save()
                    rsp = {
                        'resCode':'1',
                        'message':'State is Update succesfully'
                    }
                    return Response(rsp,status=status.HTTP_200_OK)
                else:
                        rsp={
                "resCode":'0',
                'message':'Select state name is not valid'}
                return Response(rsp,status=status.HTTP_200_OK)
        else:
            rsp={
            "resCode":'0',
            'message':'Unable to fetach data '}
            return Response(rsp,status=status.HTTP_200_OK)
        

    def delete(self,request,pk):
        if pk is not None:
            try:
                check_id = StateName.objects.get(pk=pk)
            except CountryName.DoesNotExist:
                rsp = {
                    "resCode":'0',
                    'message':'Please select correct state name ',
                }
                return Response(rsp,status=status.HTTP_200_OK)
            else:
                check_id.delete()
                rsp = {'rspCode':'1','message':'State has been deleted succesfully'}    
        else:
            rsp = {
            'resCode':'0',
            "message":"Sorry, State name is not valid",
        }
        return Response(rsp,status=status.HTTP_200_OK)

    def get(self,request,pk=None):        
        if pk is not None:
            try:
                state_id = StateName.objects.get(pk=pk)
            except StateName.DoesNotExist:
                rep={
                    'resCode':"0",
                    'message':'State name is not valid',
                }
                return Response(rep,status=status.HTTP_200_OK)
            else:
                serializer = StateSerializers(state_id)
                rep={
                    'resCode':'1',
                    'result':serializer
                }
                return Response(rep,status=status.HTTP_200_OK)
        else:
            state_data = StateName.objects.all()
            serializer = StateSerializers(state_data,many=True)
            rep = {'resCode':'1','result':serializer.data}
            return Response(rep,status=status.HTTP_200_OK)

class CityChanges(APIView):

    def post(self,request):
        city_ser = CityCreateSerializers(data=request.data)
        if city_ser.is_valid():
            city_ser.save()
            rsp = {
                'resCode':'1',
                'message':'City create succesfully'
            }
            return Response(rsp,status=status.HTTP_200_OK)
        rsp = {
            'resCode':'0',
            "message":"Sorry, City name is already exist",
            "serializerError":city_ser.errors,
        }
        return Response(rsp,status=status.HTTP_200_OK)

    def patch(self,request,pk,format=None):
        if pk is not None:
            try:
                city_id = CityName.objects.get(pk=pk)
            except CityName.DoesNotExist:
                rsp = {
                'resCode':'0',
                "message":"Sorry, Please enter exist city"}
                return Response(rsp,status=status.HTTP_200_OK)
            else:

                print(city_id,request.data)
                city_ser = CityCreateSerializers(city_id,data=request.data, partial=True)
                if city_ser.is_valid():
                    city_ser.save()
                    rsp = {
                        'resCode':'1',
                        'message':'City create succesfully'
                    }
                    return Response(rsp,status=status.HTTP_200_OK)
                else:
                    rsp = {
                    'resCode':'0',
                    "message":"Sorry,Unable to city requested data" }
                return Response(rsp,status=status.HTTP_200_OK)
        else:
            rsp = {
                        'resCode':'0',
                        'message':'Invalid city '
                    }
            return Response(rsp,status=status.HTTP_200_OK)

    def delete(self,request):
        payload = request.data
        try:
            ids = loads(payload.get("ids"))
        except Exception as e:
            rsp = {
                "resCode":'0',
                'message':'Requesting city(s) is missing',
                'message1':e
            }
            return Response(rsp,status=status.HTTP_200_OK)
        else:
            if len(ids):
                try :
                    checkData = CountryName.objects.filter(pk__in=ids)
                except Exception as e:
                    rsp={
                        'resCode':'0',"message":'Requesting city is not found',
                        }
                    return Response(rsp,status=status.HTTP_200_OK)
                else:
                    checkData.delete()
                rsp = {
                    'rspCode':'1','message':'Country has been deleted succesfully'
                }
                return Response(rsp,status=status.HTTP_200_OK)
            rsp={"rspCode":'0',"message":"Requesting country(s) missing"}
            return Response(status=status.HTTP_200_OK)
      



        
from json import loads
class CountryPagination(ListAPIView):
    queryset = CountryName.objects.all()
    serializer_class = CountrySerializers
    filter_backends = [OrderingFilter,SearchFilter]
    pagination_class = GenericPagiantion
    ordering_fields = ['name','description']
    search_fields = ['name','description']

class StatePagination(ListAPIView):
    queryset = StateName.objects.all()
    serializer_class = StateSerializers
    filter_backends = [OrderingFilter,SearchFilter]
    pagination_class = GenericPagiantion
    ordering_fields = ['name','countryId__name']
    search_fields = ['name','countryId__name']

class CityPagination(ListAPIView):
    queryset = CityName.objects.all()
    serializer_class = CitySerializers
    filter_backends = [OrderingFilter,SearchFilter]
    pagination_class = GenericPagiantion
    ordering_fields = ['name','country__name','state__name','latitude','longitude']
    search_fields = ['name','country__name','state__name','latitude','longitude']
