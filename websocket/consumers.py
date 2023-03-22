from channels.generic.websocket import (
    WebsocketConsumer, AsyncJsonWebsocketConsumer,AsyncConsumer,SyncConsumer
)
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from django.core.cache import cache
from asgiref.sync import sync_to_async
from chart.models import *
from chart.tasks import *


from celery.result import AsyncResult
import time




"""
AsyncConsumer
    they are accepted multiple connections 
    they are data deliver same time same 



SyncConsumer 
    if one connection is executed data deliver to the client therefore other connection is not accepted 
    they are accepted multiple connections but they deliver data one by one 

    
Channel Layers :- First In First Out
    Use 
        Redis Channel Layer :- 
            use for production env
            pip install channels_redis

        In-Mermory Channel Layer :- local use env  (but now i am use Redis channel )
    
    Channel :- single use commnication with only one channel 
    Groups :- It is commbination of multiple channel is called group , e.g :- broadcasting 
    Message :- must be a dict , they need to be serializers

"""


"""cache.clear()
cache.set()
cache.delete('some-key-prefix')
"""


class ScoketConnection(AsyncConsumer):
        
    async def websocket_connect(self,event):
        await self.send({
            "type":"websocket.accept",
        })
        resp = "WebSocket connection established successfully"
        await self.send({
                "type": "websocket.send",
                "text": resp,
        })


    async def websocket_receive(self,event):
        print(event,'recieve message')

        while True:
            resp = await db_to_redis_data_move(event)
            time.sleep(2)

            print("websocket details",resp)
            

            await self.send({
                "type": "websocket.send",
                "text":json.dumps(resp,indent=4, sort_keys=True, default=str),
            })


    async def websocket_disconnect(self,event):
        print(event,'Websocket is disconnected')
        await self.send({
            "type": "websocket.close"
        })
        
        raise StopConsumer
 

@sync_to_async
def db_to_redis_data_move(payload):
    print(payload)
    name = payload.get('text')
    name = eval(json.loads(name))
    print(name,'name')
    if name is None:
        return "Please send device name"
    else:
        task_id =get_device_details_send_to_websocket(name)
        print(task_id)
        return task_id


        




# ------------------------------------------ For Study -------------------------------------------

class ForInforamtion(WebsocketConsumer):
    """
    if we have number of large data in for loop then i'm use
        time.sleep(1)
    they are send all data in same time 
        not like one by one 
    that is mazer isuue so i'am use (async json web socket)  
    """
    def connect(self):
        self.room_name = "test_connection"
        self.room_group_name = "test_connection_group"
        self.accept()
        self.send(text_data=json.dumps({'name':self.room_name}))

    def receive(self, text_data):
        pass

    def disconnect(self, message):
        pass

"""
If we are using group and channel layer funtionlity, we should use channel_redis in setting.py
But you can use websocket without rediss (group and channel layer,channel name can't be use)

"""

class SyncConnectionForInforamtion(SyncConsumer):
    
    def websocket_connect(self,event):
        self.send({
            "type":"websocket.accept",
        })
        resp = "Invalid input please send valid input"
        self.send({
                "type": "websocket.send",
                "text": f"{resp}",
            })


    def websocket_receive(self,event):
        print(event,'recieve message from clent end')
        self.send({
                "type": "websocket.send",
                "text": "message sent to client",
            })


    def websocket_disconnect(self,event):
        print(event,'Websocket is disconnected')

        self.send({
            "type": "websocket.close"
        })
        
        raise StopConsumer