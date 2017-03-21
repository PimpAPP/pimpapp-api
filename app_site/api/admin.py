from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

from .models import Catador
from .models import Material
from .models import MobileCatador
from .models import MobileCooperative
from .models import Mobile
from .models import LatitudeLongitude
from .models import Collect
from .models import PhotoCollectUser
from .models import PhotoCollectCatador
from .models import Residue
from .models import PhotoResidue
from .models import GeorefResidue
from .models import RatingCatador
from .models import RatingCooperative
from .models import PhotoCooperative
from .models import Partner
from .models import Cooperative
from .models import PhotoBase
from .models import PhotoCatador
from .models import GeorefCatador

from .forms import DaysWeekWorkAdminForm


class DaysWeekWorkAdmin(admin.ModelAdmin):
    form = DaysWeekWorkAdminForm


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profiles'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Catador, DaysWeekWorkAdmin)
admin.site.register(Material, SimpleHistoryAdmin)
admin.site.register(LatitudeLongitude, SimpleHistoryAdmin)
admin.site.register(Collect)
admin.site.register(PhotoCollectUser)
admin.site.register(PhotoCollectCatador)
admin.site.register(Residue)
admin.site.register(PhotoResidue)
admin.site.register(GeorefResidue)
admin.site.register(RatingCatador)
admin.site.register(RatingCooperative)
admin.site.register(PhotoCooperative)
admin.site.register(Partner)
admin.site.register(Cooperative)
admin.site.register(MobileCatador)
admin.site.register(MobileCooperative)
admin.site.register(PhotoBase)
admin.site.register(PhotoCatador)
admin.site.register(Mobile)
admin.site.register(GeorefCatador)
