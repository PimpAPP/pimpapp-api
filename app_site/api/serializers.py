from rest_framework import serializers
from rest_framework import filters

from .models import ProfileInfo
from .models import Rating
from .models import Photo
from .models import Carroceiro
from .models import Material
from .models import LatitudeLongitude


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('carroceiro', 'created_on',
                  'freight', 'large_objects', 'demolition_waste',
                  'e_waste', 'paper', 'glass', 'plastic', 'metal',
                  'wood', 'cooking_oil')


class LatitudeLongitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatitudeLongitude
        fields = ('carroceiro', 'created_on',
                  'latitude', 'longitude', 'address')


class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = ('carroceiro', 'created_on',
                  'name', 'mno', 'has_whatsapp', 'address',
                  'region', 'address', 'region', 'city',
                  'has_motor_vehicle', 'carroca_pimpada')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('pk', 'user', 'carroceiro', 'created_on',
                  'rating', 'comment')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('pk', 'carroceiro', 'created_on',
                  'full_photo', 'thumbnail')


class CarroceiroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carroceiro
        fields = ('pk', 'catador_type', 'geolocation',
                  'profile_info', 'materials')

    geolocation = LatitudeLongitudeSerializer(required=False)
    profile_info = ProfileInfoSerializer(required=False)
    materials = MaterialSerializer(required=False)
