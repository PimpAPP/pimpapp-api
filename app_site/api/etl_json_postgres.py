import requests
import os
import django

# PYTHONPATH should the on env
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_site.settings")
# django.setup()

####################################################################

from .models import Catador

####################################################################

url = 'http://www.usereco.com/static/usereco-20170308-100803S.json'
r = requests.get(url)
join_dict = r.json()


for key, catador in join_dict.items():

    obj, created = Catador.objects.get_or_create(mongo_hash=catador['_id'])
    if created:
        print(catador)
        obj.load_mongo_obj(catador)
