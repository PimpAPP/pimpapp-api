from urllib.parse import urlparse

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app_site.api.models import ResiduePhoto


class FileUploadTests(APITestCase):

    def setUp(self):
        self.tearDown()
        u = User.objects.create_user('test', password='test',
                                     email='test@test.test')
        u.save()

    def tearDown(self):
        try:
            u = User.objects.get_by_natural_key('test')
            u.delete()

        except ObjectDoesNotExist:
            pass
        ResiduePhoto.objects.all().delete()

    def _create_test_file(self, path):
        f = open(path, 'w')
        f.write('test123\n')
        f.close()
        f = open(path, 'rb')
        return {'datafile': f}

    def test_upload_file(self):
        url = reverse('residue-list')
        data = self._create_test_file('/tmp/test_upload')

        # assert authenticated user can upload file
        token = Token.objects.get(user__username='test')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('created', response.data)

        self.assertTrue(urlparse(
            response.data['datafile']).path.startswith('/media'))

        self.assertEqual(response.data['owner'],
                       User.objects.get_by_natural_key('test').id)

        self.assertIn('created', response.data)

        # assert unauthenticated user can not upload file
        client.logout()

        response = client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
