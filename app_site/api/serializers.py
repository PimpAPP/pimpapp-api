from rest_framework import serializers

from views.models import ProfileInfo
from views.models import Rating
from views.models import Photo

class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = ('pk', 'name', 'mno', 'has_whatsapp', 'address', 'region',
            'address', 'region', 'city', 'has_motor_vehicle',
            'carroca_pimpada')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating', 'comment')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('full_photo', 'thumbnail')
