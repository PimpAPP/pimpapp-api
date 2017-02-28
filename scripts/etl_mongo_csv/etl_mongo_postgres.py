import os, sys
import pymongo

import sys, os, django
# PYTHONPATH should the on env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_site.settings")
django.setup()

####################################################################

from api.models import Carroceiro

####################################################################

client = pymongo.MongoClient("mongodb://recopimp:*******@ds025399.mlab.com:25399/recopimp")
db = client['recopimp']

join_dict = {}
for catador in db['carroceiros'].find():
    join_dict[catador["id"]] = catador

for tel_info in db['telephones'].find():
    del tel_info['_id']
    join_dict[tel_info['catador_id']].update(tel_info)

for addr_info in db['addresses'].find():
    del addr_info['_id']
    join_dict[addr_info['catador_id']].update(addr_info)

for geo_info in db['geolocations'].find():
    del geo_info['_id']
    join_dict[geo_info['catador_id']].update(geo_info)


for key, catador in join_dict.items():

    obj, created = Carroceiro.objects.get_or_create(mongo_hash=catador['_id'])
    if created:
        print(catador)
        obj.load_mongo_obj(catador)
