from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.authtoken import views

from .views import CatadorViewSet, add_statistic
from .views import CollectViewSet
from .views import UserViewSet
from .views import CooperativeViewSet
from .views import ResidueViewSet
from .views import MaterialsViewSet
from .views import NearestCatadoresViewSet
from .views import CustomObtainAuthToken
from .views import cadastro_catador
from .views import cadastro_cooperativa
from .views import export_catadores_xls
from .views import edit_catador
from .views import edit_cooperativa
from .views import get_docs
from .views import PartnerViewSet

router = routers.DefaultRouter()

router.register(r'nearest-catadores', NearestCatadoresViewSet,
                'nearest-catadores')
router.register(r'users', UserViewSet)
router.register(r'residues', ResidueViewSet, base_name='residue')
router.register(r'catadores', CatadorViewSet)
router.register(r'collect', CollectViewSet)
router.register(r'materials', MaterialsViewSet)
router.register(r'cooperatives', CooperativeViewSet, base_name='cooperative')
router.register(r'partners', PartnerViewSet, base_name='partners')


urlpatterns = [
    url(r'^api-token-auth/', CustomObtainAuthToken.as_view()),
    url(r'^export/xls/$', export_catadores_xls, name='export_catadores_csv'),
    url(r'^', include(router.urls)),
    url(r'cadastro_catador/$', cadastro_catador),
    url(r'edit_catador/$', edit_catador),
    url(r'cadastro_cooperativa/$', cadastro_cooperativa),
    url(r'add_statistic/$', add_statistic),
    url(r'edit_cooperativa/$', edit_cooperativa),
    url(r'get_docs/([0-9]{1})/$', get_docs)
]
