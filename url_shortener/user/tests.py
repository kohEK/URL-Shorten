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
        response = self.client.get('/api/users')
        # print(response.status_code) -> 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        # print(self.users)

        for user_response, user in zip(response.data['results'], self.users[::-1]):
            user_response = Munch(user_response)
            self.assertEqual(user_response['id'], user.id)
            self.assertEqual(user_response['username'], user.username)

    def test_should_create(self):
        print('test_create')
        data = {'username': 'abc', 'password': '1111'}
        # data에는 필요한 값을 딕셔너리 형태로 넣어주자 ****
        response = self.client.post('/api/users', data=data)

        user_response = Munch(response.data)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])

    def test_should_get(self):  # check GET: api/users/<int:pk> running
        print('test_get')
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/users/{user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = Munch(response.data)
        self.assertEqual(user_response.id, user.id)
        self.assertEqual(user_response.username, user.username)

    def test_should_update(self):
        print('test_update')
        user = self.users[0]
        prev_username = user.username

        data = {'username': 'new', 'password': '2222'}
        self.client.force_authenticate(user=user)
        response = self.client.put(f'/api/users/{user.id}', data=data)

        user_response = Munch(response.data)

        self.assertTrue(user_response.id)
        self.assertNotEqual(user_response.username, prev_username)
        self.assertEqual(user_response.username, data['username'])


    def test_should_deactivate(self):
        print('test_deactivate')
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/deactivate')
        print(User.objects.filter(id=user.id))
        self.assertFalse(User.objects.filter(id=user.id).exists())








