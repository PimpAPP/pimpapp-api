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
from .views import CooperativeViewSet
from .views import ResidueViewSet

router = routers.DefaultRouter()

router.register(r'carroceiro', CarroceiroViewSet)
router.register(r'^carroceiro/(?P<carroceiro>\d+)/comments$',
                RatingByCarroceiroViewSet, base_name='carroceiro-comments')
router.register(r'^carroceiro/(?P<carroceiro>\d+)/photos$',
                PhotoByCarroceiroViewSet, base_name='carroceiro-photos')
router.register(r'georef', LatitudeLongitudeViewSet)
router.register(r'rating', RatingViewSet)
#router.register(r'photo', PhotoViewSet)
#router.register(r'mobile', MobileViewSet)
router.register(r'collect', CollectViewSet)
router.register(r'users', UserViewSet)
router.register(r'cooperatives', CooperativeViewSet, base_name='cooperative')
router.register(r'residues', ResidueViewSet, base_name='residue')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
