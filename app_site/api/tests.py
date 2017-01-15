import json

from django.contrib.auth.models import AnonymousUser, User
from rest_framework.authtoken.models import Token

from django.test import TestCase, RequestFactory
from django.test import Client

from rest_framework.test import APIClient
from rest_framework.test import APITestCase


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

        json_obj = {
            "catador_type": "C",
            "name": "João da Silva",
        }

        response = self.client.post('/api/carroceiro/', json_obj, format='json')

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
            expected
        )

