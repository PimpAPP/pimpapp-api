from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Carroceiro
from .models import Material
from .models import Phone
from .models import LatitudeLongitude
from .models import Rating
from .models import Photo
from .models import Collect

admin.site.register(Carroceiro, SimpleHistoryAdmin)
admin.site.register(Material, SimpleHistoryAdmin)
admin.site.register(Phone, SimpleHistoryAdmin)
admin.site.register(LatitudeLongitude, SimpleHistoryAdmin)
admin.site.register(Rating, SimpleHistoryAdmin)
admin.site.register(Photo, SimpleHistoryAdmin)
admin.site.register(Collect)