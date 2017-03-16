from django.conf.urls import url

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
router.register(r'georef', LatitudeLongitudeViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'photo', PhotoViewSet)
router.register(r'mobile', MobileViewSet)
router.register(r'collect', CollectViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    # Example
    url('^carroceiro/(?P<carroceiro>\d+)/comments$',
        RatingByCarroceiroViewSet.as_view()),
    url('^carroceiro/(?P<carroceiro>\d+)/photos$',
        PhotoByCarroceiroViewSet.as_view()),
    url(r'^residues/$', ResidueListAPIView.as_view(), name='residue-list'),
    url(r'^residues-create/$', ResidueCreateAPIView.as_view(), name='residue-create'),
    url(r'^residues-location-create/$', ResidueLocationCreateAPIView.as_view(), name='residue-location-create'),
    url(r'^residues-location-create/$', ResidueLocationCreateAPIView.as_view(), name='residue-location-create'),
    url(r'^residues-photo-create/$', ResiduePhotoCreateAPIView.as_view(), name='residue-photo-create'),
]

urlpatterns += router.urls
