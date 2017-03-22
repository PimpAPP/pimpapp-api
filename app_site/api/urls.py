from django.conf.urls import url, include

from rest_framework import routers

from .views import CatadorViewSet
from .views import RatingViewSet
from .views import CollectViewSet
from .views import UserViewSet
from .views import CooperativeViewSet
from .views import ResidueViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'residues', ResidueViewSet, base_name='residue')
router.register(r'catadores', CatadorViewSet)
router.register(r'collect', CollectViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'cooperatives', CooperativeViewSet, base_name='cooperative')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
