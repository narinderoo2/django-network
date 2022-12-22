from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields = ['email','address','username','first_name','last_name',
        'phone_number','flag','user_timezone']

    def validate(self, attrs):
        
        if(not attrs['first_name'] or len(attrs['first_name']) < 15):
            print(len(attrs['first_name']),'--------------------')
            raise serializers.ValidationError('This field must be an even number.')
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)


#  email = models.EmailField(unique=True)
#     address = models.CharField(max_length=30, blank=True)
#     phone_number=models.CharField(blank=True,max_length=20,null=True)
#     flag=models.CharField(default='in',max_length=10)
#     user_timezone = models.CharField(max_length=250, null=True, blank=True, default="Asia/Kolkata")
#     create_at = models.D


    class Meta:
        mode = UserProfile
        fields = ('email',
            'password',
            'username',
            'first_name',
            'last_name',
            'groups',
            'phone_number',
            'address',
            'date_joined',
            
        )
        extra_kwargs = {
            'first_name' :{'requried':True},
            'groups' :{'requried':True}
        }


    def create(self, validated_data):
        user = UserProfile.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'])

        user.set_password(validated_data['password'])
        user.save()

        return user

    # def create(self, validated_data):
    #     print(validated_data,'=<<<0-------------')
    #     # groups_data = validated_data.pop('groups')
    #     password = validated_data.pop('password')

    #     user = UserProfile.objects.create(**validated_data)
    #     # for group_data in groups_data:
    #     #     user.groups.add(group_data)
    #     user.set_password(password)
    #     user.save()
    #     return user 