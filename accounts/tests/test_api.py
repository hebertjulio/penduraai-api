from django.urls import reverse

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APITestCase

from rest_framework_api_key.models import APIKey


class ApiTestCase(APITestCase):

    def test_user(self):
        _, api_key = APIKey.objects.create_key(name='My Api Key')

        data = {
            'name': 'Fulano', 'email': 'fulano@mail.br',
            'password': '12345', 'pin': '1234'
        }

        self.do_signup('v1', api_key, data)

        token = self.do_login('v1', api_key, data['email'], data['password'])

        self.get_profile_list('v1', token['access'])
        self.get_current_user('v1', token['access'])
        self.get_profile('v1', token['access'])

    def do_signup(self, version, api_key, data):
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + api_key)
        kwargs = {'version': version}
        url = reverse('accounts:signup', kwargs=kwargs)
        resp = self.client.post(url, format='json', data=data)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

    def do_login(self, version, api_key, email, password):
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + api_key)
        kwargs = {'version': version}
        url = reverse('accounts:token_obtain_pair', kwargs=kwargs)
        data = {'email': email, 'password': password}
        resp = self.client.post(url, format='json', data=data)
        self.assertEqual(resp.status_code, HTTP_200_OK)
        token = resp.json()
        return token

    def get_profile_list(self, version, access):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        headers = {'HTTP_PROFILE': 'PK %s' % 1}
        kwargs = {'version': version}
        url = reverse('accounts:profile_list', kwargs=kwargs)
        resp = self.client.get(url, {}, format='json', **headers)
        self.assertEqual(resp.status_code, HTTP_200_OK)

    def get_profile(self, version, access):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        headers = {'HTTP_PROFILE': 'PK %s' % 1}
        kwargs = {'version': version, 'pk': 1}
        url = reverse('accounts:profile_detail', kwargs=kwargs)
        resp = self.client.get(url, format='json', **headers)
        self.assertEqual(resp.status_code, HTTP_200_OK)

    def get_current_user(self, version, access):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        headers = {'HTTP_PROFILE': 'PK %s' % 1}
        kwargs = {'version': version}
        url = reverse('accounts:current_user_detail', kwargs=kwargs)
        resp = self.client.get(url, format='json', **headers)
        self.assertEqual(resp.status_code, HTTP_200_OK)
