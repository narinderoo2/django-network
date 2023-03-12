from rest_framework import serializers
from .models import *



class ChartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartDetails
        fields = ('name','time','ram','battery','cpu','modified')


