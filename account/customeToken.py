from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import *

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    class Meta:
        models=UserProfile
        fields=['email','password']


    def get_tokens_for_user(self, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, request):
        email = request.get('email')
        password = request.get('password')
        user_details = UserProfile.objects.filter(email=email).first()

        if user_details is not None:
            if user_details.is_active : 
                user = authenticate(email=email, password=password)
                if user is not None:
                    get_Token = self.get_tokens_for_user(user)
                    return {
                        'errorMessage': 'Successfully login',
                        'resultCode': '1',
                        'access_token': str(get_Token.access_token),
                        'refresh_token': str(get_Token),
                    }
                else:
                    return {
                    'errorMessage': 'Invalid credentials',
                    'resultCode': '0',
                    }
            else:
                return {
                    'errorMessage': 'User is not activate',
                    'resultCode': '0',
                }
                
        else:
            return {
                'errorMessage': 'User does not exists',
                'resultCode': '0',
            }
      