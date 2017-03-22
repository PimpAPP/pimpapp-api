import json

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Catador, Material
from .tests_general import BaseTestCase


class CatadorTestCase(BaseTestCase, APITestCase):
    expected = {'collects': [], 'safety_kit': False, 'moderation_status': 'P',
                'has_family': None, 'kg_week': None, 'georef_m2m': [],
                'slug': None, 'nickname': 'apelido', 'name': 'João da Silva',
                'carroca_pimpada': False, 'user': 1, 'works_since': None,
                'id': 1, 'country': None, 'photos': [], 'catador_type': 'C',
                'rating_m2m': [], 'materials_collected': [1],
                'mongo_hash': None, 'has_motor_vehicle': False,
                'minibio': None, 'address_base': None, 'city': None,
                'region': None, 'phones': [], 'is_locked': False
                }

    def setUp(self):
        super(CatadorTestCase, self).setUp()

        self.material = Material(name='Material test',
                                 description='description test')
        self.material.save()

        self.catador = Catador.objects.create(
            name='teste', user=self.user, nickname='Nickname')
        self.catador.save()
        self.catador.materials_collected.add(self.material)

    def test_get_all(self):
        response = self.client.get(path='/api/catadores/', format='json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(str(response.content, encoding='utf-8'))
        self.assertTrue(result['count'] > 0)

        result = json.dumps(result['results'][0])
        self.assertJSONEqual(result, self.expected)

    def test_get_by_id(self):
        response = self.client.get(
            path='/api/catadores/' + self.catador.id, format='json')

        self.assertEqual(response.status_code, 200)

        result = json.loads(str(response.content, encoding='utf-8'))
        result = json.dumps(result)
        self.assertJSONEqual(result, self.expected)

    def test_create_catador(self):
        user = User.objects.create_user(
            username='test_create', email='tester@dummy.com', password='top_secret')
        json_obj = {
            "catador_type": "C",
            "name": "João da Silva",
            "materials_collected": [1],
            "nickname": "apelido",
            "user": user.id
        }

        # Test create one
        response = self.client.post('/api/catadores/', json_obj, format='json')
        self.assertEqual(response.status_code, 201)

        self.expected['user'] = user.id
        self.expected['id'] = response.data['id']

        result = json.loads(str(response.content, encoding='utf-8'))
        result = json.dumps(result)
        self.assertJSONEqual(result, self.expected)
