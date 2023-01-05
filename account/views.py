from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from commonutils.pagination import GenericPagiantion
from .serializers import *


class UserProfileView(APIView):
    def post(self,request):
        user_serializer = RegisterSerializer(data=request.data)
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
                'resultDescription':user_serializer.errors
            }
            return Response(resp, status=status.HTTP_401_UNAUTHORIZED)

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


from django.core.mail import send_mail
from django.conf import settings


from utils.account.account_email import *

class EmailCheck(APIView):

    def post(self,request):
        payload = request.data
        ser = EmailCheckSerializer(data=payload)
        if ser.is_valid():

            result = send_otp('user_name', 'narender.singh@echelonedge.com', '222')
           
            print(result,'resultresult')
            # send_mail(
            # subject='Add an eye-catching subject',
            # message='Write an amazing message',
            # from_email=settings.EMAIL_HOST_USER,
            # recipient_list=['narender.singh@echelonedge.com'])

            resp = {
                'errorMessage': 'Verify email adress succesfully',
                'resultCode': '1',
            }
            return Response(resp, status=status.HTTP_200_OK)
        else:
            resp = {
                'errorMessage': 'Please enter valid email adress ',
                'resultCode': '0',
                'resultDescription':ser.errors
            }
            return Response(resp, status=status.HTTP_404_NOT_FOUND)


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


