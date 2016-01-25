from django.contrib import admin
from .models import Carroceiro


class CarroceiroAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'phone', 'address')

admin.site.register(Carroceiro, CarroceiroAdmin)

