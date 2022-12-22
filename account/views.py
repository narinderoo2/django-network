from django.http import HttpResponse,JsonResponse
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserProfileView(APIView):
    
    def post(self,request):
        payload = request.data
        print(payload)
        if payload :

            email = payload.get('email')
            first_name = payload.get('first_name')
            groups = payload.get('groups')
            password = payload.get('password')
            user_timezone = payload.get("user_timezone")
            confirm_password = payload.get('confirm_password')

            # print(payload)
            user_serializer = RegisterSerializer(data=payload)
            print(user_serializer,'----------=>>>>>>>>')
            if user_serializer.is_valid():
                user_serializer.save()

                
                resp = {
                            'resultCode': '1',
                            'resultDescription': 'user is created succesfully'
                        }
                return Response(resp, status=status.HTTP_200_OK)
            else:
                resp = {
                    'errorMessage': 'User with this email already exist',
                    'resultCode': '0',
                    'resultDescription': 'Please fill the form correctly'
                }
                return Response(resp, status=status.HTTP_200_OK)
        else : 

            resp = {
                        'resultCode': '0',
                        'resultDescription': 'Required fields are missing'
                    }
            return Response(resp, status=status.HTTP_200_OK)
            

    def get(self,request):
        user_se = UserSerializer()
        try:
            resp = {
                        'results': '1',
                        'data': '2',
                        'resultCode': '1',
                        'resultDescription': 'Requested user data'
                    }
            return Response(resp, status=status.HTTP_200_OK)
            
        except Exception as e:
            resp = {
                        'results': 'user_ser.data',
                        'data': 'ser_ser.data',
                        'resultCode': '0',
                        'resultDescription': 'Requested user data'
                    }
            
            
            return Response(resp, status=status.HTTP_200_OK)



from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from commonutils.pagination import GenericPagiantion


class UserPaginationOrder(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    filter_backends = [OrderingFilter,SearchFilter]
    pagination_class = GenericPagiantion
    ordering_fields = ['id', 'username','first_name','last_name',
        'email','is_active','phone_number',        ]
    search_fields = ['id', 'username',
        'first_name','last_name','email','is_active','phone_number',
        ]


