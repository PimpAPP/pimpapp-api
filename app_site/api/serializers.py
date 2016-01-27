from rest_framework import serializers

from .models import ProfileInfo
from .models import Rating
from .models import Photo
from .models import Carroceiro
from .models import Materials
from .models import LatitudeLongitude


class MaterialsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Materials
        fields = ('paper', 'freight', 'large_objects')


class LatitudeLongitudeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LatitudeLongitude
        fields = ('latitude', 'longitude', 'address')


class ProfileInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = ('pk',
            'user', 'carroceiro', 'created_on', 'moderation_status'
            'name', 'mno', 'has_whatsapp', 'address', 'region',
            'address', 'region', 'city', 'has_motor_vehicle',
            'carroca_pimpada')


class CarroceiroSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Carroceiro
        fields = ('pk', 'geolocation', 'profile_info', 'materials')

    geolocation = LatitudeLongitudeSerializer(required=False)
    profile_info = ProfileInfoSerializer(required=False)
    materials = MaterialsSerializer(required=False)


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ('pk',
            'user', 'carroceiro', 'created_on', 'moderation_status'
            'rating', 'comment')


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ('pk',
            'user', 'carroceiro', 'created_on', 'moderation_status'
            'full_photo', 'thumbnail')
