import json
from typing import Tuple

from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status

from .models import User
from .serializers import UserSerializer, UserBasicSerializer



def create_user(unique_id: str) -> Tuple[User, str]:
    password = 'test_password_{}'.format(unique_id)
    user = User.objects.create_user(
            username=unique_id,
            email='test_user_{}@foothub.com'.format(unique_id),
            password=password
        )
    return user, password

class TestUserCreation(APITestCase):
    ENDPOINT = '/api/create-user'
    CONTENT_TYPE = 'application/json'

    def test_create_user_400_no_username(self):
        data = {
            'email': 'test_user@foothub.com',
            'password': 'test_password'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['username'], ['This field is required.'])
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_400_no_email(self):
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['email'], ['This field is required.'])
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_400_invalid_username(self):
        data = {
            'username': 'test/user',
            'email': 'test_user@foothub.com',
            'password': 'test_password'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid username.', response.data['username'][0])
        self.assertEqual(User.objects.count(), 0)

    def create_user_400_blacklisted_username(self, blacklisted_username: str) -> None:
        data = {
            'username': 'me',
            'email': 'test_user@foothub.com',
            'password': 'test_password'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'], ['Username not allowed.'])
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_400_blacklisted_username(self):
        blacklisted_usernames = ['me']

        for username in blacklisted_usernames:
            self.create_user_400_blacklisted_username(username)

    def test_create_user_400_repeated_username(self):
        vasco_user, _ = create_user('vasco')

        data = {
            'username': vasco_user.username,
            'email': 'test_user@foothub.com',
            'password': 'test_password'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'], ['user with this username already exists.'])
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_400_invalid_email(self):
        data = {
            'username': 'test_user',
            'email': 'test_user.foothub.com',
            'password': 'test_password'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], ['Enter a valid email address.'])
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_400_repeated_email(self):
        vasco_user, _ = create_user('vasco')

        data = {
            'username': 'test_user',
            'email': vasco_user.email,
            'password': 'test_password'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], ['user with this email already exists.'])
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_400_no_password(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@foothub.com'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'], ['This field is required.'])
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_400_invalid_password(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@foothub.com',
            'password': 'a'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'], ['Ensure this field has at least 8 characters.'])
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_200(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@foothub.com',
            'password': 'test_password'
        }

        response = self.client.post(self.ENDPOINT, json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

        self.assertEqual(User.objects.count(), 1)


class TestUserAuthentication(APITestCase):
    ENDPOINT = '/api/token-auth'
    CONTENT_TYPE = 'application/json'

    SERIALIZER = UserSerializer

    def setUp(self):
        self.user, password = create_user('auth101')
        self.assertEquals(User.objects.all().count(), 1)

        self.data = {
            'username': self.user.username,
            'password': password
        }

    def test_serialization(self):
        expected_params = ['id', 'username', 'email']

        data = self.SERIALIZER(self.user).data

        for param in data:
            self.assertIn(param, expected_params)

    def test_get_token_400(self):
        data = {
            'username': self.user.email,
            'password': 'wrong_password'
        }

        response = self.client.post(self.ENDPOINT, data=json.dumps(data), content_type=self.CONTENT_TYPE)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_token_200(self):
        response = self.client.post(self.ENDPOINT, data=json.dumps(self.data), content_type=self.CONTENT_TYPE)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_get_protected_resource_400(self):
        url = '/api/users/{}/'.format(self.user.username)

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response.data['detail'], 'Authentication credentials were not provided.')

        response = self.client.get(url, **{'HTTP_AUTHORIZATION': 'Token {}'.format('s0meBrok3nTok1n')})
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response.data['detail'], 'Invalid token.')

    def test_get_protected_resource_200(self):
        response = self.client.post(self.ENDPOINT, data=json.dumps(self.data), content_type=self.CONTENT_TYPE)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

        url = '/api/users/{}/'.format(self.user.username)
        token = response.data['token']

        response = self.client.get(url, **{'HTTP_AUTHORIZATION': 'Token {}'.format(token)})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], self.user.username)
        self.assertEquals(response.data['email'], self.user.email)
        self.assertFalse('password' in response.data)




