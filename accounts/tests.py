import random
import string

from django.test import TestCase
from django.urls import reverse, resolve

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APITestCase

from rest_framework_api_key.models import APIKey

from faker import Faker

from .views import (
    UserListView, UserDetailView, LoggedUserDetailView,
    LoggedUserDeactivateView, TokenObtainPairView, TokenRefreshView
)

from .models import User


class UserUrlsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        faker = Faker(['pt_BR'])

        cls.user = User.objects.create(
            name=faker.name(), email=faker.email(),
            password=''.join(random.sample(string.ascii_lowercase*10, 10))
        )

    def test_resolves(self):
        self.resolve_user_list_url()
        self.resolve_user_detail_url()
        self.resolve_logged_user_detail_url()
        self.resolve_logged_user_deactivate_url()
        self.resolve_token_obtain_pair_url()
        self.resolve_token_refresh_url()

    def resolve_user_list_url(self):
        resolve = self.resolve_by_name('accounts:user_list')
        self.assertEqual(resolve.func.cls, UserListView)

    def resolve_user_detail_url(self):
        resolve = self.resolve_by_name(
            'accounts:user_detail', pk=UserUrlsTestCase.user.id)
        self.assertEqual(resolve.func.cls, UserDetailView)

    def resolve_logged_user_detail_url(self):
        resolve = self.resolve_by_name('accounts:logged_user_detail')
        self.assertEqual(resolve.func.cls, LoggedUserDetailView)

    def resolve_logged_user_deactivate_url(self):
        resolve = self.resolve_by_name('accounts:logged_user_deactivate')
        self.assertEqual(resolve.func.cls, LoggedUserDeactivateView)

    def resolve_token_obtain_pair_url(self):
        resolve = self.resolve_by_name('accounts:token_obtain_pair')
        self.assertEqual(resolve.func.cls, TokenObtainPairView)

    def resolve_token_refresh_url(self):
        resolve = self.resolve_by_name('accounts:token_refresh')
        self.assertEqual(resolve.func.cls, TokenRefreshView)

    def resolve_by_name(self, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)


class UserApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        faker = Faker(['pt_BR'])
        _, cls.api_key = APIKey.objects.create_key(name=faker.name())
        cls.user = {
            'name': faker.name(), 'email': faker.email(),
            'password': ''.join(random.sample(string.ascii_lowercase*10, 10))
        }

    def test_user(self):
        self.user_create()
        self.token_obtain_pair()
        self.user_retriave()

    def user_create(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Api-Key ' + UserApiTestCase.api_key
        )
        url = reverse('accounts:user_list')
        res = self.client.post(url, format='json', data=UserApiTestCase.user)
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        UserApiTestCase.user.update(res.json())

    def token_obtain_pair(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Api-Key ' + UserApiTestCase.api_key
        )
        url = reverse('accounts:token_obtain_pair')
        res = self.client.post(
            url, format='json', data={
                'email': UserApiTestCase.user['email'],
                'password': UserApiTestCase.user['password']
            }
        )
        self.assertEqual(res.status_code, HTTP_200_OK)
        UserApiTestCase.user.update(res.json())

    def user_retriave(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + UserApiTestCase.user['access']
        )
        params = {'pk': UserApiTestCase.user['id']}
        url = reverse('accounts:user_detail', kwargs=params)
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, HTTP_200_OK)
