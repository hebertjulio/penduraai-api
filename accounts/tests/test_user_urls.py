import random
import string

from django.test import TestCase
from django.urls import reverse, resolve

from faker import Faker

from ..views import (
    UserListView, UserDetailView, UserChangeView,
    UserDeactivateView, TokenObtainPairView, TokenRefreshView
)

from ..models import User


class UserUrlsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        faker = Faker(['pt_BR'])
        user = User(name=faker.name(), email=faker.email(), is_active=True)
        user.set_password(
            ''.join(random.sample(string.ascii_lowercase*10, 10)))
        user.save()
        cls.user = user

    def test_resolves(self):
        self.resolve_user_list_url()
        self.resolve_user_detail_url()
        self.resolve_logged_user_detail_url()
        self.resolve_logged_user_deactivate_url()
        self.resolve_token_obtain_pair_url()
        self.resolve_token_refresh_url()

    def resolve_user_list_url(self):
        r = UserUrlsTestCase.resolve_by_name('accounts:user_list')
        self.assertEqual(r.func.cls, UserListView)

    def resolve_user_detail_url(self):
        pk = UserUrlsTestCase.user.id
        r = UserUrlsTestCase.resolve_by_name('accounts:user_detail', pk=pk)
        self.assertEqual(r.func.cls, UserDetailView)

    def resolve_logged_user_detail_url(self):
        r = UserUrlsTestCase.resolve_by_name('accounts:user_change')
        self.assertEqual(r.func.cls, UserChangeView)

    def resolve_logged_user_deactivate_url(self):
        r = UserUrlsTestCase.resolve_by_name('accounts:user_deactivate')
        self.assertEqual(r.func.cls, UserDeactivateView)

    def resolve_token_obtain_pair_url(self):
        r = UserUrlsTestCase.resolve_by_name('accounts:token_obtain_pair')
        self.assertEqual(r.func.cls, TokenObtainPairView)

    def resolve_token_refresh_url(self):
        r = UserUrlsTestCase.resolve_by_name('accounts:token_refresh')
        self.assertEqual(r.func.cls, TokenRefreshView)

    @staticmethod
    def resolve_by_name(name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
