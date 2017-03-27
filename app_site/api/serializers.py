from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Catador
from .models import Rating
from .models import Mobile
from .models import MobileCatador
from .models import PhotoResidue
from .models import LatitudeLongitude
from .models import Collect
from .models import Residue
from .models import GeorefResidue
from .models import Cooperative
from .models import UserProfile
from .models import PhotoBase
from .models import Material
from .models import GeorefCatador
from .models import PhotoCollectUser
from .models import PhotoCollectCatador


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
        user_profile = UserProfile.objects.filter(user=obj)
        if user_profile:
            return user_profile[0].avatar.url
        return ''


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
        fields = ('created_on', 'latitude', 'longitude', 'reverse_geocoding')


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = '__all__'


class MobileCatadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileCatador
        fields = ('pk', 'catador', 'mobile', 'mno', 'has_whatsapp', 'mobile_internet', 'notes')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('pk', 'author', 'created_on',
                  'rating', 'comment')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoBase
        fields = ('pk', 'created_on', 'full_photo')


class PhotoCollectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCollectUser
        fields = '__all__'


class PhotoCollectCatadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCollectCatador
        fields = '__all__'


class CollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = ('pk', 'catador_confirms', 'user_confirms', 'active',
                  'catador', 'geolocation', 'residue', 'photo_collect_user',
                  'photo_collect_catador')

    photo_collect_user = PhotoCollectUserSerializer(many=True)
    photo_collect_catador = PhotoCollectCatadorSerializer(many=True)


class CatadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catador
        exclude = ['created_on', 'mobile_m2m', 'georef_m2m']

    geolocation = LatitudeLongitudeSerializer(required=False, many=True)
    phones = MobileSerializer(required=False, many=True)
    collects = CollectSerializer(required=False, many=True)
    photos = PhotoSerializer(required=False, many=True)
    profile_photo = serializers.ImageField()


class ResiduePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoResidue
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
        model = GeorefResidue
        fields = '__all__'


class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = '__all__'


class GeorefCatadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeorefCatador
        fields = '__all__'
