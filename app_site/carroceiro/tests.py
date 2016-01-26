from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient

from .models import Carroceiro


class CarroceiroTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Carroceiro.objects.create(name='João')

    def test_create_carroceiro(self):
        pass

    def test_get_carroceiro(self):
        url = reverse('carroceiro-list')
        response = self.client.post(url, {}, format='json')
        self.assertNotEqual(response.status_code, 401)
