from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Catador
from .models import Rating
from .models import PhotoCatador
from .models import MobileCatador
from .models import ResiduePhoto
from .models import LatitudeLongitude
from .models import Collect
from .models import Residue
from .models import ResidueLocation
from .models import Cooperative
from .models import UserProfile
from .models import PhotoBase
from .models import Material


class PhotoBaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhotoBase
        fields = ['full_photo', ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'photo', 'first_name', 'last_name')

    def get_photo(self, obj):
        return PhotoBaseSerializer(obj.photobase_set, many=True).data


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('url', 'username', 'email', 'groups', 'user')

    def get_user(self, obj):
        return UserSerializer(obj.user)


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('catador', 'created_on',
                  'freight', 'large_objects', 'demolition_waste',
                  'e_waste', 'paper', 'glass', 'plastic', 'metal',
                  'wood', 'cooking_oil')


class LatitudeLongitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatitudeLongitude
        fields = ('catador', 'created_on',
                  'latitude', 'longitude', 'reverse_geocoding')


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileCatador
        fields = ('pk', 'catador', 'phone', 'mno', 'has_whatsapp', 'mobile_internet', 'notes')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('pk', 'author', 'catador', 'created_on',
                  'rating', 'comment')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoBase
        fields = ('pk', 'carroceiro', 'created_on', 'full_photo')

class CollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = ('pk', 'catador_confirms', 'user_confirms', 'active',
                  'author', 'catador', 'geolocation', 'photo_collect_user',
                  'residue')


class CatadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catador
        exclude = ['created_on', ]

    geolocation = LatitudeLongitudeSerializer(required=False)
    phones = MobileSerializer(required=False, many=True)
    collects = CollectSerializer(required=False, many=True)
    photos= PhotoSerializer(required=False, many=True)


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ResiduePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResiduePhoto
        fields = '__all__'


class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ResidueSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    materials = MaterialTypeSerializer(read_only=True, many=True)

    class Meta:
        model = Residue
        fields = '__all__'

    def get_photos(self, obj):
        return ResiduePhotoSerializer(obj.residue_photos, many=True).data

    def get_latitude(self, obj):
        try:
            return obj.residuelocation.latitude
        except:
            return None

    def get_longitude(self, obj):
        try:
            return obj.residuelocation.longitude
        except:
            return None


class ResidueLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidueLocation
        fields = '__all__'


class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = '__all__'
