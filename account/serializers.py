from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields = ['email','address','username','first_name','last_name',
        'phone_number','flag','user_timezone','is_active']

    def validate(self, attrs):
        if(not attrs['first_name'] or len(attrs['first_name']) < 15):
            raise serializers.ValidationError('This field must be an even number.')
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =  ['email','username','password','first_name','last_name','phone_number','flag','user_timezone']
        extra_kwargs = {
            'first_name':{'required':True},
        }


    def create(self, validated_data):
        user = UserProfile.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active=False
        user.save()
        return user

class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        fields = ['email']

    def validate(self,attr):
            ser_Validation = UserProfile.objects.filter(email=attr['email']).first()
            if ser_Validation is None:
                 raise serializers.ValidationError('Enter valid email address')
            return attr
    

class RoleListingSerializer(serializers.ModelSerializer):
    roleDetials = serializers.SerializerMethodField()
    class Meta:
        model = Role
        fields = ['name','id','roleDetials']


    def get_roleDetials(self,payload):
        if payload:
            get_role = Permission.objects.filter(role_id__name = payload)
            role_name = []
            if get_role:
                for row in get_role:
                    role_name.append(row.name)
                return role_name
        return []


class CreateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields= ['name']

    def validate_name(self,payload):
        if payload is None or "" or not payload:
            raise serializers.ValidationError("Name is not empty")
        else:
            check = Role.objects.filter(name=payload)
            if check :
                raise serializers.ValidationError("Name must be unique")
            else:
                return payload
                
        



class GetPermission(serializers.ModelSerializer):
    """depth revers key all value get """
    class Meta:
        model = Permission
        fields = ['id','role_id','name','createDate']
        depth = 1


class CreatePermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name']
    
    def validate_name(self,payload):
        name = payload
        if name is None or "":
            raise ValueError(f"Name cannot be empty")
        else:
            check = Permission.objects.filter(name=name)
            if check:
                raise ValueError(f"Name must be unique")
            else:
                return name




class PermissionListingSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role_id.name")
    class Meta:
        model = Permission
        fields =['role_id','name','role_name','createDate']
    
       
        
        
        




    
