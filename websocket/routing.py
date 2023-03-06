"""

WSGI - Web Server Gateway Interface 
ASGI - Asynchronous Server Gateway Interface 
        bidirectional communication

Every consumer instance has an automatically generated 
unique channel name and so can be communicated with via a 
channel layer 

Channel layer, Django channels need to store the infomation
somewhere . To avoid shuttling everything through a database, its 
recommended to use a NoSQL store like Redis

        Channel is user 
        Group is, all channel on same plateform is called group
"""


from django.urls import path
from websocket.consumers import *

websocket_urlpatterns = [
    path('ws/test/',SyncConnection.as_asgi())
]