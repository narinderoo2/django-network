from channels.generic.websocket import (
    WebsocketConsumer, AsyncJsonWebsocketConsumer,AsyncConsumer,SyncConsumer
)
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):
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

    def receive(self, *, text_data):
        pass

    def disconnect(self, message):
        pass

class NewConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_name = "new connection"
        # await (self.channel_layer.group_add)(
        #     self.room_name,self.channel_layer
        # )

        print("chaneel name", self.channel_name,self.channel_layer)
        await self.accept()
        await self.send(text_data=json.dumps({"status":"connection stable"}))



"""
If we are using group and channel layer funtionlity, we should use channel_redis in setting.py
But you can use websocket without rediss (group and channel layer,channel name can't be use)

"""

class SyncConnection(SyncConsumer):
    
    def websocket_connect(self,event):
        # async_to_sync(self.channel_layer.group_add(
        #     'programer',self.channel_name
        # ))
        self.send({
            "type":"websocket.accept",
        })
        resp = "Invalid input please send valid input"
        self.send({
                "type": "websocket.send",
                "text": f"{resp}",
            })
        # self.websocket_disconnect(event)


    def websocket_receive(self,event):
        # async_to_sync(self.channel_layer.group_send("programer",{
        #     'type':'chat.message',
        #     'message':event['text']
        # }))
        resp = "eeeee"
        self.send({
                "type": "websocket.send",
                "text": f"{resp}",
            })


    def websocket_disconnect(self,event):
        # async_to_sync(self.channel_layer.group_discard)(
        #     "programer",self.channel_name
        # )

        self.send({
            "type": "websocket.close"
        })
        
        raise StopConsumer