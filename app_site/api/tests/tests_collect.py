from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import Catador
from ..models import Collect
from ..models import Residue
from rest_framework.authtoken.models import Token


class CollectTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            email='tester@dummy.com',
            password='top_secret')

        self.json_obj = {"residue": 1}

        self.catador = Catador.objects.create(
            catador_type="C", name="João da Silva",
            nickname='joao', user=self.user)

        self.collect = Collect.objects.create(
            catador_confirms=True, user_confirms=True,
            active=True, catador=self.catador)

        self.residue = Residue.objects.create(
            description='Local residue', how_many_kilos=10, user=self.user)

        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_collect(self):
        Collect.objects.create()

        self.assertTrue(Collect.objects.all().count() > 0)

    def test_recovery_collect(self):
        response = self.client.get('/api/collect/1/', format='json')

        expected = {"pk": 1,
                    "catador_confirms": True,
                    "user_confirms": True,
                    "active": True,
                    "catador": 1,
                    'photo_collect_catador': [],
                    'residue': None,
                    "photo_collect_user": []}

        self.assertJSONEqual(str(response.content, encoding='utf-8'), expected)

    def test_user_can_have_just_one_collect_oppened(self):
        '''Usuario pode ter apenas uma coleta em aberto'''

        collect1 = Collect.objects.create(
            residue=self.residue, catador=self.catador, moderation_status='P')

        collect2 = Collect.objects.create(
            residue=self.residue, catador=self.catador, moderation_status='P')

        self.assertRaises(ValidationError, collect2.clean)
