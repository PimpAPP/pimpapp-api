from django.conf.urls import url

from . import views

"""
/carroceiro/ is the URL path from the root "app_site.urls.py" point of view to carroceiro.urls.py.
"""

urlpatterns = [
    # ex: /carroceiro/, will list all carroceiros
    url(r'^$', views.CarroceirosList.as_view(), name='carroceiro-list'),
    # ex: /carroceiro/<id>/
    url(r'^(?P<id>[0-9]+)/$', views.CarroceiroDetail.as_view(), name='carroceiro-detail'),
    # ex: /carroceiro/phone/<phone>/
    url(r'^phone/(?P<phone>\d{8,15})/$', views.CarroceiroFindByPhone.as_view(), name='carroceiro-findbyphone'),
]