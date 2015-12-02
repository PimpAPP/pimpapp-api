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
    # ex: /carroceiro/rfilter/<lat>&<long>&<radius>
    # ex: /carroceiro/rfilter/-23.5374089,-46.6399287,10/
    url(r'^rfilter/(?P<lat_1>[-|+]?\d+\.\d+),(?P<long_1>[-|+]?\d+\.\d+),(?P<radius>\d+)/$', views.CarroceiroRadiusFilter.as_view(), name='carroceiro-radius-filter')
]
