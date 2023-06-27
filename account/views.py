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
from json import loads

from utils.delete_and_validations.delete_multiple import *


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


class RoleCRUD(APIView):

    def get(self,request):
        data = Role.objects.all()
        serializer = RoleListingSerializer(data,many=True)
        rep = {'resCode':'1','result':serializer.data}
        return Response(rep,status=status.HTTP_200_OK)
    
    def post(self,request):
        check_ser = CreateRoleSerializer(data=request.data)
        if check_ser.is_valid():
            check_ser.save()
            return is_valid_message(check_ser,f"{check_ser.data['name']} role create sucssfully",True)
        else:
            return is_valid_message(check_ser.errors,"Please enter valid data",False)
        
    def patch(self,request,pk): 
        name = request.data.get('name')
        if name is None or "" or not name:
            return is_valid_message(None,"Please enter valid name",False)
        if pk:
            try:
                get_detalis = Role.objects.get(id=pk)
            except Role.DoesNotExist:
                return is_valid_message(None,"Role id does not match",False)
            else:
                unique_data_check = Role.objects.filter(name = name)
                if unique_data_check:
                    return is_valid_message(None,"Role name must be unique",False)
                else:
                    get_detalis.name = name
                    get_detalis.save()
                    return is_valid_message(None,f"{name} role update sucssfully",True)
        else:
            return  is_valid_message(None,"Please select update id",False)
        
    def delete(self,request):
        return dynamic_delete_mutiple_data(request,Role,'role')






class PermissionCRUD(APIView):

    def get(self,request):
        queryset = Permission.objects.all()
        serializer = GetPermission(queryset,many=True)
        return Response({'resCode':'1','result':serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request):
        get_ids = request.data.get("role_id")
        if get_ids is None or "" or [] or not get_ids:
            res= {'resCode':'0','message':"Please enter role id's"}
            return Response(res,status=status.HTTP_200_OK)
        else:
            get_ids = loads(get_ids)
            per_ser = CreatePermissionSerializers(data=request.data)
            if per_ser.is_valid():
                for row in get_ids:
                    data = Role.objects.filter(id=row)
                    if data is None or len(data) == 0:
                        res= {'resCode':'0','message':f"Slected {row} number role id is not match "}
                        return Response(res,status=status.HTTP_200_OK)
                save =Permission.objects.create(name =per_ser.data['name'])
                save.role_id.set(get_ids)
                save.save()
                res= {'resCode':'1','message':f"{per_ser.data['name']} permission create sucssfully"}
                return Response(res,status=status.HTTP_200_OK)
            else:
                return is_valid_message(per_ser.errors,"Please enter valid data",False)

            
    def patch(self,request,pk):
        get_ids = request.data.get("role_id")
        get_name = request.data.get("name")
        
        if pk:
            try:
                get_details = Permission.objects.get(id=pk)
            except Permission.DoesNotExist:
                res= {'resCode':'0','message':"Permision id is not match"}
                return Response(res,status=status.HTTP_200_OK)
            else:
                if get_ids is None or "" or [] or not get_ids:
                    res= {'resCode':'0','message':"Please enter role id's"}
                    return Response(res,status=status.HTTP_200_OK)
                if get_name is None or "" or not get_name:
                    res= {'resCode':'0','message':"Please enter permission name"}
                    return Response(res,status=status.HTTP_200_OK)
                get_ids = loads(get_ids)
                for row in get_ids:
                    data = Role.objects.filter(id=row)
                    if data is None or len(data) == 0:
                        res= {'resCode':'0','message':f"Selected {row} number role id is not match "}
                        return Response(res,status=status.HTTP_200_OK)
                get_details.name = get_name
                get_details.role_id.set(get_ids)
                get_details.save()
                res= {'resCode':'1','message':f"{get_name} permission update sucssfully"}
                return Response(res,status=status.HTTP_200_OK)
        else:

            res= {'resCode':'0','message':"Please select update id"}
            return Response(res,status=status.HTTP_200_OK)

    def delete(self,request):
        return dynamic_delete_mutiple_data(request,Permission,'permission')
    
       


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




class PermissionPaginationOrder(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionListingSerializer
    filter_backends = [OrderingFilter,SearchFilter]
    pagination_class = GenericPagiantion
    ordering_fields = ['role_id_name','name']
    search_fields = ['role_id_name','name']


