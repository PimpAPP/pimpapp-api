import json

from django.contrib.auth.models import User
from ..models import Catador, Material
from ..models import Mobile
from ..models import MobileCatador

from .tests_general import BaseTestCase


def new_catador():
    user = User.objects.create_user(
        username='test_create', email='tester@dummy.com', password='top_secret')

    catador = Catador.objects.create(name='Fulano', user=user)
    catador.save()
    return catador


class CatadorTestCase(BaseTestCase):
    def setUp(self):
        super(CatadorTestCase, self).setUp()

        self.material = Material(name='Material test',
                                 description='description test')
        self.material.save()

        self.catador = Catador.objects.create(
            name='João da Silva', user=self.user, nickname='Nickname')
        self.catador.save()
        self.catador.materials_collected.add(self.material)

        self.data_expected = {'collects': [], 'safety_kit': False, 'moderation_status': 'P',
                              'has_family': None, 'kg_week': None, 'geolocation': [],
                              'slug': None, 'nickname': 'Nickname', 'name': 'João da Silva',
                              'carroca_pimpada': False, 'user': 1, 'works_since': None,
                              'id': 1, 'country': None, 'photos': [], 'catador_type': 'C',
                              'materials_collected': [1], 'mongo_hash': None, 'has_motor_vehicle': False,
                              'minibio': None, 'address_base': None, 'city': None,
                              'region': None, 'phones': [], 'is_locked': False,
                              'profile_photo': None, 'how_many_days_work_week': None,
                              'cooperative': None, 'presentation_phrase': None
                              }

    def test_get_all(self):
        response = self.client.get(path='/api/catadores/', format='json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(str(response.content, encoding='utf-8'))
        self.assertTrue(result['count'] > 0)

        result = json.dumps(result['results'][0])
        self.assertJSONEqual(result, self.data_expected)

    def test_get_by_id(self):
        response = self.client.get(path='/api/catadores/{id}/'.format(id=self.catador.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.data_expected)

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

        local_expected = self.data_expected
        local_expected['user'] = user.id
        local_expected['id'] = response.data['id']
        local_expected['nickname'] = "apelido"
        local_expected['id'] = 2

        self.assertEqual(response.data, local_expected)

    def test_update_catador(self):
        json_obj = {"name": "Maria da Silva"}

        # Test update
        response = self.client.patch('/api/catadores/1/', json_obj, format='json')
        self.assertEqual(response.status_code, 200)

        local_expected = self.data_expected
        local_expected['name'] = 'Maria da Silva'

        self.assertEqual(response.data, local_expected)

    def test_update_catador_permission(self):
        user = User.objects.create_user(
            username='test_create', email='tester@dummy.com', password='top_secret')

        catador = Catador.objects.create(name='Fulano', user=user)
        catador.save()

        json_obj = {"name": "Teste permissão"}

        # Test update permission
        response = self.client.patch(
            '/api/catadores/{id}/'.format(
                id=user.id), json_obj, format='json')

        self.assertEqual(response.status_code, 403)

    def test_delete_catador(self):
        response = self.client.delete(path='/api/catadores/1/', content_type='application/json')
        self.assertEqual(response.status_code, 204)
        total = Catador.objects.all().count()
        self.assertTrue(total == 0)

    def test_delete_catador_permission(self):
        response = self.client.delete(
            path='/api/catadores/{id}/'.format(id=new_catador().id),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)

    def test_create_catador_location(self):

        data = {"moderation_status": "A", "latitude": 123, "longitude": 999,
             "reverse_geocoding": "reverse cURL"}

        # Test create one
        response = self.client.post(
            '/api/catadores/{id}/georef/'.format(id=self.catador.id),
            data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_create_catador_location_permission(self):
        user = User.objects.create_user(
            username='test_create', email='tester@dummy.com', password='top_secret')

        catador = Catador.objects.create(name='Fulano', user=user)
        catador.save()

        data = {"moderation_status": "A", "latitude": 123, "longitude": 999,
             "reverse_geocoding": "reverse cURL"}

        # Test create one
        response = self.client.post(
            '/api/catadores/{id}/georef/'.format(id=catador.id),
            data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_create_catador_mobile(self):

        data = {"phone": "123", "mno": "V", "has_whatsapp": True,
                "mobile_internet": True, "notes": "notes"}

        # Test create one
        response = self.client.post(
            '/api/catadores/{id}/phones/'.format(id=self.catador.id),
            data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_create_catador_mobile_permission(self):
        data = {"phone": "123", "mno": "V", "has_whatsapp": True,
                "mobile_internet": True, "notes": "notes"}

        # Test create one
        response = self.client.post(
            '/api/catadores/{id}/phones/'.format(id=new_catador().id),
            data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_delete_catador_mobile(self):
        m = Mobile.objects.create(
            phone='123', mno='V', has_whatsapp=True, mobile_internet=True,
            notes='Notes'
        )
        MobileCatador.objects.create(mobile=m, catador=self.catador)
        response = self.client.delete(
            path='/api/catadores/{id}/phones/'.format(id=self.catador.id),
            data={'id': m.id}
        )

        self.assertTrue(response.status_code, 204)

    def test_delete_catador_mobile_permission(self):
        m = Mobile.objects.create(
            phone='123', mno='V', has_whatsapp=True, mobile_internet=True,
            notes='Notes'
        )
        MobileCatador.objects.create(mobile=m, catador=self.catador)
        response = self.client.delete(
            path='/api/catadores/{id}/phones/'.format(id=new_catador().id),
            data={'id': m.id}
        )

        self.assertTrue(response.status_code, 403)
