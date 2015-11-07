from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Carroceiro

class CarroceiroSerializer(serializers.ModelSerializer):
    """
    Class used for serialization Carroceiro into JSON
    """
    class Meta:
        model = Carroceiro
        fields = ('id', 'name', 'type', 'phone', 'address', 'latitude', 'longitude')
