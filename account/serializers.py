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
            
       
        
        
        




    
