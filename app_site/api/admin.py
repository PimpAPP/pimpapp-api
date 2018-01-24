from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db import models
from django import forms
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
from .models import Rating
from .models import GeneralErros
from .forms import DaysWeekWorkAdminForm


# CATADOR

class PhoneInline(admin.StackedInline):
    model = MobileCatador
    can_delete = True
    verbose_name_plural = 'Telefones'

    def get_max_num(self, request, obj=None, **kwargs):
        return 2


class GeoRefInline(admin.StackedInline):
    model = GeorefCatador
    can_delete = True
    verbose_name_plural = 'Geo Ref. (Posição no mapa)'
    exclude = ['short_description']

    def get_max_num(self, request, obj=None, **kwargs):
        return 1


class MaterialInline(admin.StackedInline):
    model = Catador.materials_collected.through
    can_delete = False
    verbose_name_plural = 'Materiais'

    def get_max_num(self, request, obj=None, **kwargs):
        return 12


class CatadorAdmin(admin.ModelAdmin):
    #form
    exclude = ['mongo_hash', 'slug', 'days_week_work']
    fields = ('name', 'nickname', 'presentation_phrase', 'minibio', 'city',
              'region', 'country', 'address_base', 'number', 'address_region',
              'has_motor_vehicle', 'has_smartphone_with_internet', 'year_of_birth',
              'works_since', 'registered_by_another_user', 'another_user_name',
              'another_user_email', 'another_user_whatsapp')
    inlines = (PhoneInline, GeoRefInline, MaterialInline)

    #list
    list_filter = ('country', 'city', 'registered_by_another_user')
    search_fields = ['id', 'name', 'nickname']
    form = DaysWeekWorkAdminForm
    list_display = ('pk', 'name', 'nickname', 'get_phones', 'get_avatar', 'get_georef',
                    'city', 'region', 'address_base', 'number', 'address_region',
                    'presentation_phrase', 'get_registered_by_another_user', 'modified_date')
    filter_vertical = ['materials_collected']

    def get_avatar(self, obj):
        return True if obj.user.userprofile.avatar else False

    get_avatar.short_description = 'Possui foto?'
    get_avatar.boolean = True
    get_avatar.admin_order_field = 'userprofile__avatar'

    def get_phones(self, obj):
        return ', '.join([p.phone for p in obj.phones])

    get_phones.short_description = 'Telefone(s)'

    def get_materials(self, obj):
        return ', '.join([m.name for m in obj.materials])

    get_materials.short_description = 'Materiais que coleta'

    def get_georef(self, obj):
        geo = GeorefCatador.objects.get(catador_id=obj.id)
        res = ''
        if geo:
            res = str(geo.georef.latitude) + ', ' + str(geo.georef.longitude)

        return res

    get_georef.short_description = 'Lat/Long'

    def get_registered_by_another_user(selfs, obj):
        if obj.registered_by_another_user:
            return obj.another_user_name
        else:
            return 'Próprio catador'

    get_registered_by_another_user.short_description = 'Cadastrado por'

# USER

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profiles'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'id')
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', 'get_avatar')

    def get_avatar(self, obj):
        return True if obj.userprofile.avatar else False

    get_avatar.short_description = 'Possui foto?'
    get_avatar.boolean = True
    get_avatar.admin_order_field = 'userprofile__avatar'


class MobileAdmin(admin.ModelAdmin):
    model = Mobile

    class Media:
        js = ('scripts/main.js',)


class ErroAdmin(admin.ModelAdmin):
    list_filter = ('date', )
    search_fields = ['id', 'detail', 'date']
    list_display = ('date', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Catador, CatadorAdmin)
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
admin.site.register(Mobile, MobileAdmin)
admin.site.register(GeorefCatador)
admin.site.register(Rating)
admin.site.register(GeneralErros, ErroAdmin)
