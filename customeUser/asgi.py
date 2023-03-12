import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from websocket import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customeUser.settings')

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http":get_asgi_application(), 

    # WebSocket chat handler
    "websocket":URLRouter(routing.websocket_urlpatterns),
})



"""
    by default use get_asgi_application() 
    application 
        - we can add other protocols later
        - ASGI_APPLICATION = 'customeUser.asgi.application' add in setting.py
        - the main entry in your routing file  

"""
