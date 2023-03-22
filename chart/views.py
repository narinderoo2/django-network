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
from django.core.cache import cache

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


class PcDeviceDetails(APIView):

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
            if cache.get(get_device_details[0]['name']):
                # print(cache.get(get_device_details[0]['name']))
                pass
            else:
                cache.set(get_device_details[0]['name'],{'data':serializer.data})
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
            "message":"Sorry,device details is not find"}
            return Response(rsp,status=status.HTTP_200_OK)
        

class Download(APIView):

    def get(self,request):
        dtat = download()

        print(dtat)
        # rsp = {
        #     'resCode':'0',
        #     "message":"Sorry,device details is not find",
        #     'result':dtat}
        return FileResponse(dtat,status=status.HTTP_200_OK)



import zipfile

from django.http import HttpResponse

# from .models import Script

README_NAME = 'README.md'
README_CONTENT = """
## PyBites Code Snippet Archive
Here is a zipfile with some useful code snippets.
Produced for blog post https://pybit.es/django-zipfiles.html
Keep calm and code in Python!
"""
ZIPFILE_NAME = 'pybites_codesnippets.zip'

import zlib, sys, shutil

import csv


def download():
    try:

        response = HttpResponse(
        content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

        return response






        a = "E:\Angular Git Project\django_network"
        with zipfile.ZipFile('filesystem.zip','w') as file: # opening the zip file using 'zipfile.ZipFile' class
            file.write('log.csv')
            print('File overrides the existing files')
        with zipfile.ZipFile('filesystem.zip', 'r') as file:
            print(file.namelist())

        shutil.make_archive('archive','zip',a)


    except zipfile.BadZipFile: # if the zip file has any errors then it prints the error message which you wrote under the 'except' block
        print('Error: Zip file is corrupted')















import os, io, zipfile
from django.http import HttpResponse,FileResponse
def downloaf1():
    # Get file
    # url = 'https://some.link/img.jpg'
    # response = requests.get(url)
    # Get filename from url
    # filename = os.path.split(url)[1]
    # Create zip
    buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(buffer, 'w')
    zip_file.writestr('kkkkkkkkkkkkkkk', 'response')
    zip_file.close()
    # Return zip
    response = HttpResponse(buffer.getvalue())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename=album.zip'

    return response


import csv
import io
import zipfile
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from rest_framework.views import APIView

class ExportZip(APIView):

    async def get(self,request):
        csv_datas = await self.build_multiple_csv_files()
        
        temp_file = io.BytesIO()
        with zipfile.ZipFile(
             temp_file, "w", zipfile.ZIP_DEFLATED
        ) as temp_file_opened:
            # add csv files each library
            for data in csv_datas:
                data["csv_file"].seek(0)
                temp_file_opened.writestr(
                    f"library_{data['library_name']}.csv",
                    data["csv_file"].getvalue()
                )

        temp_file.seek(0)

        print(temp_file)
        
        # put them to streaming content response 
        # within zip content_type
        response =  FileResponse(temp_file, content_type="application/zip")
        

        response['Content-Disposition'] = 'attachment;filename=Libraries.zip'
        print(response)
       
        # return Response(response,status=status.HTTP_200_OK)
        return response

    def build_multiple_csv_files(self, libraries, books):
        csv_files = []
        
        # for library in libraries.iterator():
        #     mem_file = io.StringIO()
        #     writer = csv.DictWriter(
        #         mem_file, fieldnames=self.header_data.keys()
        #     )
        #     writer.writerow(self.header_data)
            
        #     books_in_library = books.filter(libraries__in=[library.id])
        #     for book in books_in_library:
        #         book_row = self.build_book_row(book, library)
        #         writer.writerow(book_row)
            
        #     mem_file.seek(0)
            
        #     csv_files.append({
        #         "library_name": library.name,
        #         "csv_file": mem_file
        #     })
            
        return csv_files
    
    def build_book_row(self, book, library):
        row = self.header_data.copy()
        
        row["name"] = book.name
        row["library"] = library.name
        
        return row