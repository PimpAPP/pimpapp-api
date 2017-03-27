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
