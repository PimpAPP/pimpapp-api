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
        fields = ('freight', 'large_objects', 'demolition_waste',
                  'e_waste', 'paper', 'glass', 'plastic', 'metal',
                  'wood', 'cooking_oil')


class LatitudeLongitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatitudeLongitude
        fields = ('latitude', 'longitude', 'address')


class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = ('pk',
            'user', 'carroceiro', 'created_on', 'moderation_status',
            'name', 'catador_type', 'mno', 'has_whatsapp', 'address',
            'region', 'address', 'region', 'city', 'has_motor_vehicle',
            'carroca_pimpada')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('pk',
            'user', 'carroceiro', 'created_on', 'moderation_status',
            'rating', 'comment')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('pk',
            'user', 'carroceiro', 'created_on', 'moderation_status',
            'full_photo', 'thumbnail')


class CarroceiroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carroceiro
        fields = ('pk', 'catador_type', 'geolocation',
                'profile_info', 'materials') #'rating', 'photos')

    geolocation = LatitudeLongitudeSerializer(required=False)
    profile_info = ProfileInfoSerializer(required=False)
    materials = MaterialSerializer(required=False)
    #photos = PhotoSerializer(required=False)
    #rating = RatingSerializer(required=False)
