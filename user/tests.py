from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from user.models import User


class UserAuthTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_data = [{'email': 'test@test.com', 'password': 'pass1234', 'fullname': 'Test Test'},
                             {'email': 'test@test.com', 'password': 'pass1234', 'fullname': 'Test2 Test2'}]
        cls.login_data = [{'email': 'test@test.com', 'password': 'pass1234'},
                          {'email': 'nottest@test.com', 'password': 'pass1234'}]

    def test_successful_register_user(self):
        url = reverse('user_register')
        response = self.client.post(url, self.register_data[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_existing_register_user(self):
        url = reverse('user_register')
        self.client.post(url, self.register_data[0], format='json')
        response = self.client.post(url, self.register_data[1], format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        self.client.post(reverse('user_register'), self.register_data[0], format='json')
        response = self.client.post(reverse('user_login'), self.login_data[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_not_existing_user(self):
        self.client.post(reverse('user_register'), self.register_data[0], format='json')
        response = self.client.post(reverse('user_login'), self.login_data[1], format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_user(self):
        token = self.client.post(reverse('user_register'), self.register_data[0], format='json').data
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token["access"]}'}
        response = self.client.post(reverse('user_logout'), format='json', **auth_header)
        user = User.objects.get(email='test@test.com')
        outstanding_token = OutstandingToken.objects.filter(user=user)
        blacklisted_token = BlacklistedToken.objects.filter(id=outstanding_token[0].id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(blacklisted_token)

    def test_login_refresh(self):
        token = self.client.post(reverse('user_register'), self.register_data[0], format='json').data
        response = self.client.post(reverse('token_refresh'), {'refresh': token['refresh']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
