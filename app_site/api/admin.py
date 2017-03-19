from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Catador
from .models import Material
from .models import MobileCatador
from .models import MobileCooperative
from .models import LatitudeLongitude
# TODO
#from .models import Photo
from .models import Collect
from .models import PhotoCollectUser
from .models import PhotoCollectCatador
from .models import Residue
from .models import ResiduePhoto
from .models import ResidueLocation

from .models import RatingCatador
from .models import RatingCooperative

from .models import Material
from .models import PhotoCooperative
from .models import Partner
from .models import Cooperative


admin.site.register(Catador, SimpleHistoryAdmin)
admin.site.register(Material, SimpleHistoryAdmin)
admin.site.register(LatitudeLongitude, SimpleHistoryAdmin)
#admin.site.register(Photo, SimpleHistoryAdmin)
admin.site.register(Collect)
admin.site.register(PhotoCollectUser)
admin.site.register(PhotoCollectCatador)
admin.site.register(Residue)
admin.site.register(ResiduePhoto)
admin.site.register(ResidueLocation)

admin.site.register(RatingCatador)
admin.site.register(RatingCooperative)

admin.site.register(PhotoCooperative)
admin.site.register(Partner)
admin.site.register(Cooperative)
