from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.cache import cache
from .models import *
import datetime
import platform
import psutil



"""
Parameters
status (str) - Current task state.

retval (Any)- Task return value/exception.

task_id (str)- Unique id of the task.

args (Tuple)- Original arguments for the task.

kwargs (Dict)- Original keyword arguments for the task.

einfo (ExceptionInfo) - Exception information.
"""

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


@shared_task(name="device_details_save")
def getDeviceDetailsSave():
    sys_name = platform.uname()
    svmem = psutil.virtual_memory()
    device_name = f"{sys_name.system}:{sys_name.node}"
    total_ram = get_size(svmem.total)

    get_device_details = DeviceDetails.objects.filter(name=device_name)
    if get_device_details:
        print('***')

    else:
        save_details = DeviceDetails.objects.create(name=device_name,total_ram=total_ram)
        save_details.save()
    saveDeviceDetails(device_name)

    return True 


def saveDeviceDetails(device_name):
    get_details = DeviceDetails.objects.get(name=device_name)
    battery_deatils = psutil.sensors_battery()
    svmem = psutil.virtual_memory()
    cpu_use = f"{psutil.cpu_percent()}%"
    total_core = psutil.cpu_count(logical=True)
    total_ram = get_size(svmem.total)
    available_ram = get_size(svmem.available)
    used_ram = get_size(svmem.used)
    current_datetime = datetime.datetime.now() 
    bettery = battery_deatils.percent
    save_details = ChartDetails(name=get_details,ram=used_ram,cpu=cpu_use,battery=bettery,time=current_datetime)
    save_details.save()
    return




@shared_task(name="device_details_get_and_send_to_websocket")
def get_device_details_send_to_websocket(name):
    # print(kwargs,kwargs.get("name"))
    data = name
    if data:
        sys_name = platform.uname()
        device_name = f"{sys_name.system}:{sys_name.node}"
        print(data == device_name,data,device_name)
        # if(data == device_name ):
        return getDetailsOfDevice_Use_Websocket(device_name)
        # else:
            # return "Please correct device name "
    return 'name is not found ' 


def getDetailsOfDevice_Use_Websocket(device_name):
    battery_deatils = psutil.sensors_battery()
    svmem = psutil.virtual_memory()
    cpu_use = f"{psutil.cpu_percent()}%"
    used_ram = get_size(svmem.used)
    current_datetime = datetime.datetime.now() 
    bettery = battery_deatils.percent
    data = { 
      "name": device_name,
      "time": formate_change(current_datetime),
      "ram": used_ram,
      "battery": bettery,
      "cpu": cpu_use,
      "modified": formate_change(current_datetime)
    }
    return data



def formate_change(time):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ" 
    datee= datetime.datetime.strftime(time, date_format)
    return datee




# ---------------- For Testing-----------------

@shared_task(name="multiply_two_numbers")
def mul(x, y):
    # Celery recognizes this as the `multiple_two_numbers` task
    # total = x * (y * random.randint(3, 100))
    # logger.info('task add1 called. args: %s %s', total)
    # print(total,'===')


    # Store data under a-unique-key:
    cache.set('a-unique-key', 'this is a string which will be cached')

    # Later on you can retrieve it in another function:
    cache.get('a-unique-key') # Will return None if key is not found in cache

    # You can specify a default value:
    cache.get('another-unique-key', 'default value')

    total = cache.set('alldata',60*45)
    data = cache.get('alldata')
    return data


