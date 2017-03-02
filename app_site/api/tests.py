import json
import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from .models import Carroceiro
from .models import Collect


class CatadorTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@dummy.com',
            password='top_secret')

        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_carroceiro(self):

        json_obj = {
            "catador_type": "C",
            "name": "João da Silva",
        }

        response = self.client.post('/api/carroceiro/', json_obj, format='json')
        response = self.client.get('/api/carroceiro/1/', format='json')

        expected = {
            "pk": 1,
            "catador_type": "C",
            "name": "João da Silva",
            "geolocation": None,
            "address_base": None,
            "region": None,
            "city": None,
            "country": None,
            "has_motor_vehicle": False,
            "carroca_pimpada": False,
            "is_locked": False
        }

        self.assertJSONEqual(
            str(response.content, encoding='utf-8'),
            expected
        )

    def test_update_carroceiro(self):

        Carroceiro.objects.create(catador_type="C", name="João da Silva")

        json_obj = {
            "pk": 1,
            "city": "São Paulo",
        }

        response = self.client.patch('/api/carroceiro/1/', json_obj, format='json')

        expected = {
            "pk": 1,
            "catador_type": "C",
            "name": "João da Silva",
            "geolocation": None,
            "address_base": None,
            "region": None,
            "city": "São Paulo",
            "country": None,
            "has_motor_vehicle": False,
            "carroca_pimpada": False,
            "is_locked": False
        }

        self.assertJSONEqual(
            str(response.content, encoding='utf-8'),
            expected)


class GeoRefTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@dummy.com',
            password='top_secret')

        Carroceiro.objects.create(catador_type="C", name="João da Silva")

        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_create_geo(self):

        json_obj = {
            "carroceiro": 1,
            "latitude": 23.5,
            "longitude": 46.6
        }

        response = self.client.post('/api/georef/', json_obj, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.patch('/api/carroceiro/1/', json_obj, format='json')
        #ts = LatitudeLongitude.objects.get(pk=1).created_on


        expected = {
            "pk": 1,
            "catador_type": "C",
            "name": "João da Silva",
            "geolocation": {
                "carroceiro": 1,
                "latitude": 23.5,
                "longitude": 46.6,
                #"created_on": ts,
                "reverse_geocoding": ""
            },
            "address_base": None,
            "region": None,
            "city": None,
            "country": None,
            "has_motor_vehicle": False,
            "carroca_pimpada": False,
            "is_locked": False
        }

        result = json.loads(str(response.content, encoding='utf-8'))
        del result['geolocation']['created_on']
        result = json.dumps(result)

        self.assertJSONEqual(
            result,
            expected
        )


class CollectTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            email='tester@dummy.com',
            password='top_secret')

        self.json_obj = {"catador_confirms": True, "user_confirms": True,
                    "active": True, "author": self.user.id, "carroceiro": 1, "moderation_status": 'P'}

        self.carroceiro = Carroceiro.objects.create(
            catador_type="C", name="João da Silva")

        self.collect = Collect.objects.create(
            catador_confirms=True, user_confirms=True, active=True,
            author=self.user, carroceiro=self.carroceiro)

        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_collect(self):
        self.collect = Collect.objects.create(
            catador_confirms=True, user_confirms=True, active=True,
            author=self.user, carroceiro=self.carroceiro)

        response = self.client.post('/api/collect/', self.json_obj, format='json')
        self.assertEqual(response.status_code, 201)

    def test_recovery_collect(self):
        response = self.client.get('/api/collect/4/', format='json')

        expected = {"pk": 4,
                    "catador_confirms": True,
                    "user_confirms": True,
                    "active": True,
                    "author": 2,
                    "carroceiro": 2,
                    "geolocation": None,
                    "photo_collect_user": []}

        self.assertJSONEqual(str(response.content, encoding='utf-8'), expected)
