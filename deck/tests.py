from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey

from deck.models import Folder


class FolderTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        data = []
        for i in range(10):
            data.append({'folder_name': f'Folder{i}'})
        cls.folder_data = data
        cls.login_data = {'email': 'test@test.com', 'password': 'pass1234'}
        cls.register_data = {'email': 'test@test.com', 'password': 'pass1234', 'fullname': 'Test Test'}

    def setUp(self):
        api_key, key = APIKey.objects.create_key(name="test-api-key")
        self.api_key_headers = {'HTTP_X_API_KEY': key}
        self.client.post(reverse('user_register'), self.register_data, format='json', **self.api_key_headers)
        token = self.client.post(reverse('user_login'), self.login_data, format='json', **self.api_key_headers).data
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {token["access"]}'}

    def test_create_folder(self):
        response = self.client.post(reverse('folder_create'), self.folder_data[0], format='json',
                                    **self.auth_header, **self.api_key_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_folder(self):
        for folder in self.folder_data:
            response = self.client.post(reverse('folder_create'), folder, format='json',
                                        **self.auth_header, **self.api_key_headers)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('folder_list'), format='json',
                                   **self.auth_header, **self.api_key_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        folders = response.data
        self.assertEqual(len(folders), len(self.folder_data))


class DeckTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.folder_1 = Folder.objects.create(folder_name='Folder 1')
        self.folder_2 = Folder.objects.create(folder_name='Folder 2')
