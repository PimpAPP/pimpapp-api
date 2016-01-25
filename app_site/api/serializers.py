from rest_framework import serializers

from .models import ProfileInfo
from .models import Rating
from .models import Photo

class ProfileInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = ('pk',
            'user', 'carroceiro', 'created_on', 'moderation_status'
            'name', 'mno', 'has_whatsapp', 'address', 'region',
            'address', 'region', 'city', 'has_motor_vehicle',
            'carroca_pimpada')

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
