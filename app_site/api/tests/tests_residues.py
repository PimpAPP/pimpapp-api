import os
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from ..models import Residue
from ..models import Material

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResidueTestCase(APITestCase):

    def setUp(self):
        self.tearDown()

        self.u = User.objects.create_user('test', password='test',
                                     email='test@test.test')
        self.u.save()

        self.token = Token.objects.get(user__username='test')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.material = Material.objects.create(description='Metal')
        self.material.save()

        self.residue = Residue.objects.create(description='Test Residue')
        self.residue.materials.add(self.material)
        self.residue.save()

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
        """
        Certify that the API is able to receive file Upload
        :return: 201 when a file is successful uploaded
        """
        url = '/api/residues-photo-create/'

        path_to_image = os.path.join(BASE_DIR, 'tests/file-for-tests.png')
        data = {'full_photo': open(path_to_image, 'rb'),
                'moderation_status': 'A', 'mongo_hash': 'Mongo Hash', 'author': '1',
                'residue': self.residue.id}

        response = self.client.post(url, data, format='multipart')

        self.assertEquals(response.status_code, 201)

    def test_residues_create(self):
        json_obj = {
            "description": "Via tests",
            "materials": [self.material.id, ]}

        response = self.client.post('/api/residues-create/', json_obj, format='json')

        self.assertEqual(response.status_code, 201)

    def test_residues_json_format(self):
        json_obj = {
            "description": "Via tests",
            "materials": [self.material.id, ]}

        response = self.client.post('/api/residues-create/', json_obj, format='json')

        expected = {'description': 'Via tests', 'id': 2, 'latitude': None, 'longitude': None,
                    'materials': [1], 'photos': []}

        self.assertJSONEqual(
            str(response.content, encoding='utf-8'),
            expected
        )

    def test_residue_get(self):
        response = self.client.get('/api/residues/?search=1', format='json')

        expected = [{'description': 'Test Residue',
                     'id': 1, 'latitude': None, 'longitude': None,
                     'materials': [1], 'photos': [] }]

        self.assertJSONEqual(
            str(response.content, encoding='utf-8'),
            expected)

    def test_residue_location_get(self):
        json_obj = {
            "moderation_status": "A",
            "mongo_hash": "Hash",
            "latitude": 123,
            "longitude": 456,
            "reverse_geocoding": "Reverse",
            "residue": self.residue.id
        }

        response = self.client.post('/api/residues-location-create/', json_obj, format='json')

        self.assertEqual(response.status_code, 201)

    def test_residue_location_json_validation(self):
        json_obj = {
            "moderation_status": "A",
            "mongo_hash": "Hash",
            "latitude": 123,
            "longitude": 456,
            "reverse_geocoding": "Reverse",
            "residue": self.residue.id
        }

        response = self.client.post('/api/residues-location-create/', json_obj, format='json')

        expected = {'id': 1, "moderation_status": "A", "mongo_hash": "Hash", "latitude": 123.0,
            "longitude": 456.0,
            "reverse_geocoding": "Reverse",
            "residue": self.residue.id
        }

        import json

        json = json.loads(response.content.decode('utf-8'))
        del json['created_on']

        self.assertEqual(response.status_code, 201)
