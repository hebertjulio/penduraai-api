from django.test import TestCase
from django.urls import reverse, resolve

from .. import views


class UrlsTestCase(TestCase):

    def test_resolve_signup_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:signup', **kwargs)
        self.assertEqual(r.func.cls, views.SignUpView)

    def test_resolve_current_user_detail_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:current_user_detail', **kwargs)
        self.assertEqual(r.func.cls, views.CurrentUserDetailView)

    def test_resolve_token_obtain_pair_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:token_obtain_pair', **kwargs)
        self.assertEqual(r.func.cls, views.TokenObtainPairView)

    def test_resolve_token_refresh_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:token_refresh', **kwargs)
        self.assertEqual(r.func.cls, views.TokenRefreshView)

    def resolve_profile_list_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:profile_list', **kwargs)
        self.assertEqual(r.func.cls, views.ProfileListView)

    def test_resolve_profile_create_url(self):
        kwargs = {'version': 'v1', 'token': 'mytoken'}
        r = self.resolve_by_name('accounts:profile_create', **kwargs)
        self.assertEqual(r.func.cls, views.ProfileCreateView)

    def test_resolve_profile_detail_url(self):
        kwargs = {'version': 'v1', 'pk': 84}
        r = self.resolve_by_name('accounts:profile_detail', **kwargs)
        self.assertEqual(r.func.cls, views.ProfileDetailView)

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
