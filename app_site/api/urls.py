from django.conf.urls import url

from rest_framework import routers

from . import views

from .views import ProfileInfoViewSet
from .views import CarroceiroViewSet
from .views import RatingViewSet
from .views import PhotoViewSet

from .views import RatingByCarroceiroViewSet
from .views import PhotoByCarroceiroViewSet
from .views import PhoneByCarroceiroViewSet

router = routers.DefaultRouter()

router.register(r'carroceiro', CarroceiroViewSet)
#router.register(r'profile', ProfileInfoViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'photo', PhotoViewSet)

urlpatterns = [
    # Example
    url('^carroceiro/(?P<carroceiro>\d+)/rating$',
        RatingByCarroceiroViewSet.as_view()),
    url('^carroceiro/(?P<carroceiro>\d+)/photo$',
        PhotoByCarroceiroViewSet.as_view()),
    url('^carroceiro/(?P<carroceiro>\d+)/phone$',
        PhoneByCarroceiroViewSet.as_view()),
]

urlpatterns += router.urls
