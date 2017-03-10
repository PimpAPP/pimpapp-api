from django.conf.urls import url

from rest_framework import routers

from .views import CarroceiroViewSet
from .views import LatitudeLongitudeViewSet
from .views import RatingViewSet
from .views import PhotoViewSet

from .views import RatingByCarroceiroViewSet
from .views import PhotoByCarroceiroViewSet
from .views import CollectViewSet
from .views import UserViewSet

router = routers.DefaultRouter()

router.register(r'carroceiro', CarroceiroViewSet)
router.register(r'georef', LatitudeLongitudeViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'photo', PhotoViewSet)
router.register(r'collect', CollectViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    # Example
    url('^carroceiro/(?P<carroceiro>\d+)/comments$',
        RatingByCarroceiroViewSet.as_view()),
    url('^carroceiro/(?P<carroceiro>\d+)/photos$',
        PhotoByCarroceiroViewSet.as_view()),
    #url('^carroceiro/(?P<carroceiro>\d+)/phones$',
    #    PhoneByCarroceiroViewSet.as_view()),
]

urlpatterns += router.urls
