import requests
import os, django

# PYTHONPATH should the on env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_site.settings")
django.setup()
from django.contrib.auth.models import User

####################################################################

from api.models import Catador

####################################################################

def load_objects(json_dict):
    cont = 0
    for key, catador in json_dict.items():
        print(cont)
        print(catador)
        cont+=1

        email = catador['email'] if catador['email'] else 'deful@email.com'

        user, created = User.objects.get_or_create(
            username=''.join(catador['name'].split(' ')[0:3]),
            email=email
        )

        if not created:
            continue

        catador['user_id'] = user.id

        obj = Catador.objects.create(user=user)
        obj.load_mongo_obj(catador)

url = 'http://www.usereco.com/static/usereco-20170308-100803S.json'
r = requests.get(url)
join_dict = r.json()
load_objects(join_dict)
