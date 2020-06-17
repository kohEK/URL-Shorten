from munch import Munch
from django.contrib.auth.models import User
from model_bakery import baker

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


# Create your tests here.

class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = baker.make('auth.User', _quantity=3)
        self.token = Token.objects.create(user=self.users[0])

    def test_should_list(self):
        print('test_get')
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/users')
        # print(response.status_code) -> 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
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

    def test_should_login(self):
        print('test_login')
        user = baker.make('auth.User')
        password = 'password'
        # baker가 생성한 password가 암호화가 되지않도록 password를 ''로 plain password를 만들어준다. ****
        user.set_password(password)
        user.save()

        data = {'username': user.username, 'password': password}
        # print(data)
        response = self.client.post('/api/users/login', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])
        # print(response.data) {'token': '58bfda52a379ba71a9d5a7636ed6f8758f2ed1d4', 'user_id': 4}

    def test_should_logout(self):
        print('test_logout')
        user = baker.make('auth.User')
        password = 'password'

        user.set_password(password)
        user.save()

        token = Token.objects.create(user=user)
        print('token >>>>>>>>>', token)
        data = {'username': user.username, 'password': password}
        response = self.client.delete('/api/users/logout', data=data)

        # 토큰이 없는 유저가 요청을 보내서 , response 안에 토큰이 없을테니
        # 토큰이 없는지를 검사한다.

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # self.assertNotIsInstance()
        # print(response.data){'detail': 'Successfully logged out.'}
        self.assertIsNone(response.data.get(token))
        with self.assertRaises(KeyError):
            response.data['token']



        # self.fail()
