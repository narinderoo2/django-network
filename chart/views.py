from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .tasks import *
from .serializers import *
from .models import *
import datetime
import platform
import psutil
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
import json
from django.http import JsonResponse


def get_size(bytes, suffix="B"):
    """ Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
     """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


class TestingCPU(APIView):

    """
    While delay is convenient, it doesn't give you as much control as using apply_async. 
    With apply_async you can override the execution options available as attributes on the Task class 
    (see Task options). 
    In addition you can set countdown/eta, task expiry, provide a custom broker connection and more.

    """
    def get(self,request):
        sys_name = platform.uname()
        device_name = f"{sys_name.system}:{sys_name.node}"

        try:
            get_device_details = DeviceDetails.objects.filter(name__icontains=device_name).values()
        except DeviceDetails.DoesNotExist:
            rsp = {
            'resCode':'0',
            "message":"System device name is not find"}
            return Response(rsp,status=status.HTTP_200_OK)
        
        if get_device_details:
            get_all_data = ChartDetails.objects.filter(name=get_device_details[0]['id'])
            serializer = ChartDetailsSerializer(get_all_data, many=True)    
            item = [{
                'deivce_name' : get_device_details[0]['name'],
                'deivce_ram':get_device_details[0]['total_ram'],
                'data':serializer.data
            }]
            rsp = {
            'resCode':'1',
            "message":"Device details get succesfully",
            'result':item}
            return Response(rsp,status=status.HTTP_200_OK)
        else:
            rsp = {
            'resCode':'0',
            "message":"Sorry, Please enter exist city"}
            return Response(rsp,status=status.HTTP_200_OK)
        
