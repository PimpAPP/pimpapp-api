from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

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
from .models import PhotoCooperative
from .models import Partner
from .models import Cooperative
from .models import PhoneNumbers
from .models import PhotoBase
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
admin.site.register(PhotoCooperative)
admin.site.register(Partner)
admin.site.register(Cooperative)
admin.site.register(PhoneNumbers)
admin.site.register(PhotoBase)
