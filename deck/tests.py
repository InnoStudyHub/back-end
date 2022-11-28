from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from deck.models import Folder
from user.models import User


class FolderTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        data = []
        for i in range(100):
            data.append({'folder_name': f'Folder{i}'})
        cls.folder_data = data
        cls.login_data = {'email': 'test@test.com', 'password': 'pass1234'}
        cls.register_data = {'email': 'test@test.com', 'password': 'pass1234', 'fullname': 'Test Test'}

    def setUp(self):
        self.client.post(reverse('user_register'), self.register_data, format='json')
        token = self.client.post(reverse('user_login'), self.login_data, format='json').data
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token["access"]}'}

    def test_create_folder(self):
        response = self.client.post(reverse('folder_create'), self.folder_data[0], format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_folder(self):
        for folder in self.folder_data:
            response = self.client.post(reverse('folder_create'), folder, format='json', **self.auth_header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('folder_list'), format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        folders = response.data
        self.assertEqual(len(folders), len(self.folder_data))
