from django.test import TestCase, client

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase




class UrlsTestCase(APITestCase):
    pass
    # def setUp(self) -> None:
    #
    #
    #
    # def test_url_get(self):
    #     print('get_origin_url')
    #     url = "http://www.example.com"
    #     response = self.client.get('api/urls')
    #
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.fail()