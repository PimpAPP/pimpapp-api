from django.conf.urls import url, include

from rest_framework import routers

from .views import CarroceiroViewSet
from .views import LatitudeLongitudeViewSet
from .views import RatingViewSet
from .views import PhotoViewSet
from .views import MobileViewSet

from .views import RatingByCarroceiroViewSet
from .views import PhotoByCarroceiroViewSet
from .views import CollectViewSet
from .views import UserViewSet
from .views import ResidueListAPIView
from .views import ResidueCreateAPIView
from .views import ResidueLocationCreateAPIView
from .views import ResiduePhotoCreateAPIView

router = routers.DefaultRouter()

router.register(r'carroceiro', CarroceiroViewSet)
router.register(r'^carroceiro/(?P<carroceiro>\d+)/comments$',
                RatingByCarroceiroViewSet, base_name='Carroceiro')
router.register(r'^carroceiro/(?P<carroceiro>\d+)/photos$',
                PhotoByCarroceiroViewSet, base_name='Carroceiro')
router.register(r'georef', LatitudeLongitudeViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'photo', PhotoViewSet)
router.register(r'mobile', MobileViewSet)
router.register(r'collect', CollectViewSet)
router.register(r'users', UserViewSet)
router.register(r'residues', ResidueListAPIView, base_name='Residue')
router.register(r'residues-create', ResidueCreateAPIView, base_name='Residue')
router.register(r'residues-location-create', ResidueLocationCreateAPIView, base_name='Residue')
router.register(r'residues-photo-create', ResiduePhotoCreateAPIView, base_name='Residue')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
