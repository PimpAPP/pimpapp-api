import json

from django.contrib.auth.models import User
from ..models import Catador, Material, LatitudeLongitude, GeorefCatador
from ..models import Mobile
from ..models import MobileCatador
#
# from .tests_general import BaseTestCase
from rest_framework.test import APITestCase


class CatadorTestCase(APITestCase):

    @classmethod
    def setUpTestData(self):
        catador = {
            'name': 'Catador 1',
            'nickname': 'Catador nickname',
            'presentation_phrase': 'Frase teste',
            'minibio': 'Minibio teste',
            'phones': [
                {
                    'phone': '1234-1234',
                    'has_whatsapp': 1
                }
            ]
        }

        user = {
            'username': 'user1',
            'password': '123',
            'email': 'user@gmail.com',
            'first_name': 'Catador',
            'last_name': '1'
        }

        u = User.objects.create_user(username=user['username'],
                                     password=user['password'],
                                     email=user['email'])

        user['id'] = u.pk

        c = Catador.objects.create(
            name=catador['name'],
            nickname=catador['nickname'],
            presentation_phrase=catador['presentation_phrase'],
            minibio=catador['minibio'],
            user=u)

        catador['id'] = c.pk
        catador['user'] = u.pk

        location = {
            'latitude': -16.7377569,
            'longitude': -43.8682667
        }

        georeference = LatitudeLongitude.objects.create(
            latitude=location['latitude'],
            longitude=location['longitude'])

        GeorefCatador.objects.create(georef=georeference, catador=c)

        phones = [
            {
                'phone': '1234-1234',
                'has_whatsapp': 1
            }
        ]

        self.data = {
            'catador': catador,
            'user': user,
            # avatar: avatar,
            'location': location,
            'phones': phones
        }

    def test_get_catador(self):
        response = self.client.get(path='/api/catadores/1/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_edit_catador(self):
        self.data['catador']['nickname'] = 'Catador Nickname 2'
        response = self.client.post('/api/edit_catador/', self.data, format='json')
        self.assertEqual(response.status_code, 200)
