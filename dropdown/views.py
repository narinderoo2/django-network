from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Role,UserGroup

from .serializers import *



class DropDownListing(ListAPIView):

    def get(self,request):
        payload = request.GET.get('filter')
        if payload is None or "":
            res= {'resCode':'0','message':"filter is missing in query param"}
            return Response(res,status=status.HTTP_200_OK)
        else:
            if payload == "role":
                get_list = Role.objects.all()
                return serializer_listing(get_serializer_class(Role,['id','name']),get_list,'role')
            elif payload == 'group':
                get_list = UserGroup.objects.all()
                return serializer_listing(get_serializer_class(UserGroup,['id','name']),get_list,'role')
            else:
                res= {'resCode':'0','message':"Not get all lisintg",'result':[]}
                return Response(res,status=status.HTTP_200_OK)



def serializer_listing(seriali_name,list,name):
    ser = seriali_name(list,many=True)
    res= {'resCode':'1','message':f"Get all {name} lisintg",'result':ser.data}
    return Response(res,status=status.HTTP_200_OK)



#  ___Dynamic Serializer create for listing___

def get_serializer_class(name,item):
    DynamicSerializer.Meta.model = name
    DynamicSerializer.Meta.fields = item
    return DynamicSerializer  

