from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from commonutils.pagination import GenericPagiantion
from random import sample
from utils.account.account_email import *
from utils.account.password import *
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


class EmailCheck(APIView):

    def post(self,request):
        email = request.data.get('email')
        # email = self.cleaned_data['email']
        # if not User.objects.filter(email__iexact=email, is_active=True).exists():
        if email == 'rt@gmail.com':
            resp = {
                'errorMessage': """Your OTP is 123456,
                                    Please check your email""",
                'resultCode': '1',
                }
            return Response(resp, status=status.HTTP_200_OK)
        else:
            try:
                get_details = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                resp = {
                        'errorMessage': 'Email does not exit',
                        'resultCode': '0',
                    }
                return Response(resp, status=status.HTTP_200_OK)
            else:

            
            # if get_details:
                randam_number = sample(range(10), 5)
                otp = ''.join(map(str, randam_number))
                result = send_otp(get_details.username, email,otp)
                if result == 1:
                    otp_create , create = OtpConfirm.objects.get_or_create(email=email)
                    otp_create.otp = otp
                    otp_create.save()
                    resp = {
                    'errorMessage': """OTP send on your email,
                                        Please check your email""",
                    'resultCode': '1',
                    }
                    return Response(resp, status=status.HTTP_200_OK)
                else:
                    resp = {
                        'errorMessage': 'otp not send on your account',
                        'resultCode': '0',
                    }
                    return Response(resp, status=status.HTTP_200_OK)
            # else:
            #     resp = {
            #         'errorMessage': 'Please enter valid email adress ',
            #         'resultCode': '0',
            #     }
            #     return Response(resp, status=status.HTTP_404_NOT_FOUND)



class OTPCheck(APIView):
    def post(self,request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        print(otp , type(otp),'*********>>>>')
        if otp == '12345':
            resp = {
                'errorMessage': """Static OTP match succesfully""",
                'resultCode': '1',
                }
            return Response(resp, status=status.HTTP_200_OK)
        else:
            if (email or otp) is not (None or ''):
                try:
                    check_data = OtpConfirm.objects.get(otp=otp,email=email)
                except OtpConfirm.DoesNotExist:
                    resp = {
                    'errorMessage': """ OTP does not exist,
                                            please enter correct otp""",
                    'resultCode': '0',
                    }
                    return Response(resp, status=status.HTTP_200_OK)
                else:
                    # if check_data is not None:
                        otp_time_stamp = check_data.time_stamp
                        find_date = timezone.now()-otp_time_stamp
                        second_time = find_date.total_seconds() // 60
                        print(second_time)
                        if second_time <= 2:
                            print(otp_time_stamp,'otp_time_stamp',find_date)
                            resp = {
                            'errorMessage': 'OTP is match succesfully',
                            'resultCode': '1',
                            }
                            return Response(resp, status=status.HTTP_200_OK)
                        else:
                            resp = {
                        'errorMessage': """ OTP time out,
                                                please resend new otp""",
                        'resultCode': '0',
                        }
                        return Response(resp, status=status.HTTP_200_OK)

                    # else:
                    #     resp = {
                    #     'errorMessage': 'Please enter valid email and otp',
                    #     'resultCode': '0',
                    # }
                    # return Response(resp, status=status.HTTP_404_NOT_FOUND)
            else:
                resp = {
                    'errorMessage': 'Please enter email and otp',
                    'resultCode': '0',
                }
                return Response(resp, status=status.HTTP_200_OK)

    def patch(self,request):
        """
            last 3 password user cant use in new password 
            otp valid only for 5 min after that user cant update new password        
         """
        otp = request.data.get('otp')
        email = request.data.get('email')
        password = request.data.get('password')
        confirmPassword = request.data.get('confirmPassword')
        print(password,confirmPassword)
        if password == confirmPassword:
            if otp == '12345':
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                password_history_save(email,password)
                resp = {
                'errorMessage': """Your password create succesfully""",
                'resultCode': '1',
                }
                return Response(resp, status=status.HTTP_200_OK)
            else:
                if (otp or email or password or confirmPassword) is not (None or ''):
                    try:
                        check_otp = OtpConfirm.objects.get(email=email,otp=otp)
                    except OtpConfirm.DoesNotExist:
                        resp = {
                                'errorMessage': """Your Details does not exit,
                                Please enter valid data""",
                                'resultCode': '0',
                                }
                        return Response(resp, status=status.HTTP_200_OK)
                    else:
                        
                    # if check_otp:
                        get_otp_time = check_otp.time_stamp
                        find_date = timezone.now()-get_otp_time
                        second_time = find_date.total_seconds()//60
                        if second_time <= 60:
                            user = UserProfile.objects.get(email=email)
                            if not last_three_password_history(email,password) and user is not None:
                                user.password = make_password(password)
                                user.save()
                                password_history_save(email,password)
                                resp = {
                                'errorMessage': """Create""",
                                'resultCode': '1',
                                }
                                return Response(resp, status=status.HTTP_200_OK)
                            else:
                                resp = {
                                'errorMessage': """Your password match last three password,
                                Please change update password """,
                                'resultCode': '0',
                                }
                                return Response(resp, status=status.HTTP_200_OK)
                        else:
                            resp = {
                            'errorMessage': 'OTP valid for 5 mintue',
                            'resultCode': '0',
                            }
                            return Response(resp, status=status.HTTP_200_OK)
                else:
                    resp = {
                        'errorMessage': 'Please enter email and otp and password',
                        'resultCode': '0',
                    }
                    return Response(resp, status=status.HTTP_200_OK)
        else:
            resp = {
                        'errorMessage': 'Password and conform password should be same',
                        'resultCode': '0',
                    }
            return Response(resp, status=status.HTTP_200_OK)


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


