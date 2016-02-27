from rest_framework import serializers
from rest_framework import filters

from .models import Rating
from .models import Photo
from .models import Phone
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
                  'latitude', 'longitude', 'reverse_geocoding')


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('phone', 'mno', 'has_whatsapp', 'notes')


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
                'name', 'address_base', 'region', 'city',
                'country', 'has_motor_vehicle', 'carroca_pimpada',
                'is_locked')

    geolocation = LatitudeLongitudeSerializer(required=False)
    #materials = MaterialSerializer(required=False)
