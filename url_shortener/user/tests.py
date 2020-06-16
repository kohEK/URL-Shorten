
from munch import Munch
from django.contrib.auth.models import User
from model_bakery import baker

from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.

class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = baker.make('auth.User', _quantity=3)

    def test_should_list(self):
        print('test_get')
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/users/')
        # print(response.status_code) -> 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(self.users)

        for user_response, user in zip(response.data, self.users):

            user_response = Munch(user_response)
            self.assertEqual(user_response['id'], user.id)
            self.assertEqual(user_response['username'], user.username)
        self.fail()

