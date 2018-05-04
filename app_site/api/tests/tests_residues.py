import os
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from ..models import Residue
from ..models import Material
from ..models import PhotoResidue

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

        self.residue = Residue.objects.create(description='Test Residue',
                                              user=self.u, quantity='S')
        self.residue.materials.add(self.material)
        self.residue.save()

    def tearDown(self):
        try:
            u = User.objects.get_by_natural_key('test')
            u.delete()

        except ObjectDoesNotExist:
            pass
        PhotoResidue.objects.all().delete()

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
        curl exemple: curl -i -X POST -H "Content-Type: multipart/form-data"
        -F "full_photo=@/home/xtreme/gp.png"  -F "author=1" -F
        "residue=1" http://localhost:8000/api/residues/1/photos/
        -H 'Authorization: Token 3d6f97ff0e934f040dd798f20c90f187d98730a4'
        """
        url = '/api/residues/1/photos/'

        path_to_image = os.path.join(BASE_DIR, 'tests/file-for-tests.png')

        data = {'full_photo': open(path_to_image, 'rb'), 'author': '1',
                'residue': self.residue.id}

        response = self.client.post(url, data, format='multipart')

        self.assertEquals(response.status_code, 200)

    def test_residues_create(self):
        json_obj = {
            "description": "Via tests",
            "materials": [self.material.id, ],
            'quantity': 'S'}

        response = self.client.post('/api/residues/', json_obj, format='json')

        self.assertEqual(response.status_code, 201)

    def test_residues_update(self):
        json_obj = {
            "description": "Via tests alterado",
            "materials": [self.material.id, ],
            'quantitu': 'CS'}

        response = self.client.patch('/api/residues/{id}/'.format(
            id=self.residue.id), json_obj, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['description'], 'Via tests alterado')

    # def test_residues_json_format(self):
    #     json_obj = {
    #         "description": "Via tests",
    #         "materials": [self.material.id, ],
    #         'quantity': 'CR'}
    #
    #     response = self.client.post('/api/residues/', json_obj, format='json')
    #
    #     expected = {'active': True, 'description': 'Via tests', 'id': 2,
    #                 'latitude': None, 'longitude': None, 'materials': [],
    #                 'photos': [], "user": None, 'nearest_catadores': [],
    #                 'reverse_geocoding': None, 'quantity': 'CR'}
    #
    #     self.assertJSONEqual(
    #         str(response.content, encoding='utf-8'),
    #         expected
    #     )

    def test_residue_get(self):
        response = self.client.get(path='/api/residues/1/', format='json')
        self.assertEqual(response.status_code, 200)

