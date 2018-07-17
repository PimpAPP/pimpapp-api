from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from ..models import Mobile


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
            phone='11999999999',
            mno='TIM',
            has_whatsapp=True,
            mobile_internet=True
        )

        self.assertTrue(Mobile.objects.all().count() > 0)


class UsersTestCase(APITestCase):
    """
    Tests to assert that the API is able to manage Django Users
    """
    @classmethod
    def setUpTestData(self):
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

        u = User.objects.get(pk=2)
        self.assertEqual(u.email, 'joao_teste_create@pimp.com')

    # def test_user_update(self):
    #
    #     json_obj = {
    #         'pk': 1,
    #         'email': 'joao2@pimp.com',
    #     }
    #
    #     response = self.client.patch('/api/users/1', json_obj, format='json', follow=True)
    #     self.assertEqual(response.status_code, 200)
    #
    #     u = User.objects.get(pk=1)
    #     self.assertEqual(u.email, 'joao2@pimp.com')
