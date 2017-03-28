from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import Catador
from ..models import Collect
from ..models import Material
from ..models import Residue
from rest_framework.authtoken.models import Token


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

        self.residue = Residue.objects.create(
            description='Local residue', how_many_kilos=10, user=user.id)

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

        import pdb;pdb.set_trace()
        collect1 = Collect.objects.create(
            residue=self.residue, catador=self.catador, moderation_status='P',
            user=self.user
        )

        collect2 = Collect.objects.create(
            residue=self.residue, catador=self.catador, moderation_status='P',
            user=self.user
        )

        self.assertRaises(ValidationError, collect2.clean)

    def test_user_must_select_at_least_one_material(self):
        '''Usuário é obrigado a marcar quais materia estão na coleta'''

        material = Material(catador=self.catador)

        self.assertRaises(ValidationError, material.clean)