from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Carroceiro
from .models import Material
from .models import Phone
from .models import LatitudeLongitude
from .models import Photo
from .models import Collect
from .models import PhotoCollectUser
from .models import PhotoCollectCatador
from .models import Residue
from .models import ResiduePhoto
from .models import ResidueLocation
from .models import Rating
from .models import MaterialType
from .forms import DaysWeekWorkAdminForm


class DaysWeekWorkAdmin(admin.ModelAdmin):
    form = DaysWeekWorkAdminForm

admin.site.register(Carroceiro, DaysWeekWorkAdmin)
admin.site.register(Material, SimpleHistoryAdmin)
admin.site.register(Phone, SimpleHistoryAdmin)
admin.site.register(LatitudeLongitude, SimpleHistoryAdmin)
admin.site.register(Photo, SimpleHistoryAdmin)
admin.site.register(Collect)
admin.site.register(PhotoCollectUser)
admin.site.register(PhotoCollectCatador)
admin.site.register(Residue)
admin.site.register(ResiduePhoto)
admin.site.register(ResidueLocation)
admin.site.register(Rating)
admin.site.register(MaterialType)
