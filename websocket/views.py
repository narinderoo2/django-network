from django.shortcuts import render
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.consumer import AsyncConsumer


# class WebsocketConnection(AsyncConsumer):
#     print('--------------->>>>>>>>>>>>.')
#     async def websocket_connect(self, message):
#         print(message,'------')
#         await self.send({
#             "type": "websocket.accept",
#         })

#     async def websocket_receive(self, message):
#         # await asyncio.sleep(1)
#         await self.send({
#             "type": "websocket.send",
#             "text": "pong",
#         })




class Checkconnection():
    pass