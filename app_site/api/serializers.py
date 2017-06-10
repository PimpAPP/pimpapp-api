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
from .models import PhotoCooperative
from .models import Partner


class PhotoBaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhotoBase
        fields = ['full_photo', ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'photo', 'first_name',
                  'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def get_photo(self, obj):
        user_profile = UserProfile.objects.filter(user=obj)
        if user_profile:
            return user_profile[0].avatar.url
        return ''

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        if validated_data.get('password'):
            user.set_password(validated_data['password'])
        else:
            raise Exception('Password is required')

        user.save()
        return user


class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=20)

    class Meta:
        app_label = 'nectar_admin'
        model = User
        fields = ('password', 'old_password')


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
        fields = ('id', 'name', 'description')


class LatitudeLongitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatitudeLongitude
        fields = ('latitude', 'longitude', 'reverse_geocoding')


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = '__all__'


class MobileCatadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileCatador
        fields = ('pk', 'catador', 'mobile', 'mno', 'has_whatsapp',
                  'mobile_internet', 'notes')


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
        fields = ('pk', 'status', 'motivo', 'catador_confirms',
                    'user_confirms', 'active', 'catador', 'geolocation',
                    'residue', 'photo_collect_user', 'photo_collect_catador')

    photo_collect_user = PhotoCollectUserSerializer(many=True)
    photo_collect_catador = PhotoCollectCatadorSerializer(many=True)


class CatadorsPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catador
        fields = ['id', 'geolocation']
    geolocation = LatitudeLongitudeSerializer(required=False, many=True)


class CatadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catador
        exclude = ['created_on', 'mobile_m2m', 'georef_m2m', 'rating_m2m']

    geolocation = LatitudeLongitudeSerializer(required=False, many=True)
    phones = MobileSerializer(required=False, many=True)
    collects = CollectSerializer(required=False, many=True)
    photos = PhotoSerializer(required=False, many=True)
    profile_photo = serializers.CharField(read_only=True)
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email


class PhotoResidueSerializer(serializers.ModelSerializer):
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
    reverse_geocoding = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    materials = MaterialSerializer(read_only=True, many=True)
    nearest_catadores = serializers.SerializerMethodField()

    def create(self, validated_data):
        r = Residue.objects.create(**validated_data)
        r.user = self.context['request'].user
        r.save()
        return r

    class Meta:
        model = Residue
        fields = '__all__'

    def get_nearest_catadores(self, obj):
        return obj.nearest_catadores

    def get_photos(self, obj):
        return PhotoResidueSerializer(obj.residue_photos, many=True).data

    def get_reverse_geocoding(self, obj):
        try:
            return obj.residue_location.reverse_geocoding
        except:
            return None

    def get_latitude(self, obj):
        try:
            return obj.residue_location.latitude
        except:
            return None

    def get_longitude(self, obj):
        try:
            return obj.residue_location.longitude
        except:
            return None


class ResidueLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeorefResidue
        fields = '__all__'


class PhotoCooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCooperative
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class CooperativeSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    partners = PartnerSerializer(many=True)

    class Meta:
        model = Cooperative
        exclude = ['mobile_m2m', 'rating_m2m']

    phones = MobileSerializer(required=False, many=True)

    def get_photos(self, obj):
        return PhotoCooperativeSerializer(obj.photocooperative_set, many=True).data


class GeorefCatadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeorefCatador
        fields = '__all__'
