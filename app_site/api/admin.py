from django.contrib import admin

from .models import Carroceiro
from .models import Material
from .models import LatitudeLongitude
from .models import Rating
from .models import Photo
from .models import ProfileInfo
from .models import ProfileInfoHistoric

admin.site.register(Carroceiro)
admin.site.register(Material)
admin.site.register(LatitudeLongitude)
admin.site.register(Rating)
admin.site.register(Photo)
admin.site.register(ProfileInfo)
admin.site.register(ProfileInfoHistoric)
