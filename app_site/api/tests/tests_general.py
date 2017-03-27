import json
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from ..models import Catador
from ..models import Collect
from ..models import Mobile
from ..models import Material


class BaseTestCase(APITestCase):
    user = None

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@dummy.com',
            password='top_secret')

        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class MobileTestCase(BaseTestCase):

    def test_mno(self):

        Mobile.objects.create(
            catador=self.catador,
            phone='11999999999',
            mno='TIM',
            has_whatsapp=True,
            mobile_internet=True
        )

        # Deveria falhar

    def test_update(self):

        p = Mobile.objects.create(
            catador=self.catador,
            phone='11999999999',
            mno='TIM',
            has_whatsapp=True,
            mobile_internet=True
        )

        json_obj = {
            'phone': '(21) 99468-8149',
            'mno': 'O',
            'has_whatsapp': True,
            'mobile_internet': True
        }

        response = self.client.patch('/api/mobile/1/',
                                        json_obj, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/mobile/1/', format='json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(str(response.content, encoding='utf-8'))
        del result['pk']
        del result['catador']
        del result['notes']
        result = json.dumps(result)

        self.assertJSONEqual(
            result,
            json.dumps(json_obj)
        )


class GeoRefTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@dummy.com',
            password='top_secret')

        Catador.objects.create(catador_type="C", name="João da Silva")

        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_geo(self):

        json_obj = {
            "catador": 1,
            "latitude": 23.5,
            "longitude": 46.6
        }

        response = self.client.post('/api/georef/', json_obj, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.patch('/api/catador/1/', json_obj, format='json')

        expected = {
            'how_many_collect_week': None,
            'region': None,
            'internet_outside': False,
            'id': 1,
            'works_since': None,
            'city': None,
            'moderation_status': 'P',
            'how_years_many_collect': None,
            'carroca_pimpada': False,
             'materials_collected': [],
            'is_locked': False,
            'minibio': None,
            'mongo_hash': None,
            'phones': [],
            'slug': None, 'has_motor_vehicle': False,
            'geolocation': {
                'longitude': 46.6, 'latitude': 23.5,
                            'reverse_geocoding': '',
                            'catador': 1
            },
            'catador_type': 'C',
            'how_many_collect_day': None,
            'country': None,
            'safety_kit': False,
            'name': 'João da Silva',
            'days_week_work': None,
            'has_family': False,
            'user': None,
            'address_base': None
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
                    "active": True, "author": self.user.id, "catador": 1, "moderation_status": 'P'}

        self.catador = Catador.objects.create(
            catador_type="C", name="João da Silva")

        self.collect = Collect.objects.create(
            catador_confirms=True, user_confirms=True,
            active=True, catador=self.catador)

        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_collect(self):
        """
        Assert that the API is able to create a new Collect
        :return:
        """
        Collect.objects.create(
            catador_confirms=True, user_confirms=True,
            active=True, catador=self.catador)

        response = self.client.post('/api/collect/', self.json_obj, format='json')
        self.assertEqual(response.status_code, 201)

    def test_recovery_collect(self):
        response = self.client.get('/api/collect/1/', format='json')

        expected = {"pk": 1,
                    "catador_confirms": True,
                    "user_confirms": True,
                    "active": True,
                    "author": 1,
                    "catador": 1,
                    "geolocation": None,
                    "photo_collect_user": []}

        self.assertJSONEqual(str(response.content, encoding='utf-8'), expected)

    def test_user_can_have_just_one_collect_oppened(self):
        '''Usuario pode ter apenas uma coleta em aberto'''

        collect1 = Collect.objects.create(
            catador_confirms=True, user_confirms=True, active=True,
            author=self.user, catador=self.catador, moderation_status='P')

        collect2 = Collect.objects.create(catador_confirms=True, user_confirms=True, active=True,
                                          author=self.user, catador=self.catador, moderation_status='P')

        self.assertRaises(ValidationError, collect2.clean)

    def test_user_must_select_at_least_one_material(self):
        '''Usuário é obrigado a marcar quais materia estão na coleta'''

        material = Material(catador=self.catador)

        self.assertRaises(ValidationError, material.clean)


class UsersTestCase(APITestCase):
    """
    Tests to assert that the API is able to manage Django Users
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@dummy.com',
            password='top_secret')

        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.json_obj = {
            'username': 'Joao',
            'email': 'joao_teste_create@pimp.com',
            'password': 'password$@#@$#%123'
        }

    def test_create_user(self):
        """
        Assert that the API is able to create commum Django Users
        :return: 201 as a status code
        """
        response = self.client.post('/api/users/', self.json_obj, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_was_created(self):
        """
        Assert that a user was correct created by count the users occurrences
        on data base
        :return: 2 as a user counting
        """
        self.client.post('/api/users/', self.json_obj, format='json')
        self.assertTrue(User.objects.get(email='joao_teste_create@pimp.com'))
