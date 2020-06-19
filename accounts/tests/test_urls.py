from django.test import TestCase
from django.urls import reverse, resolve

from .. import views


class UrlsTestCase(TestCase):

    def test_resolves(self):
        self.resolve_signup_url('v1')
        self.resolve_current_user_detail_url('v1')
        self.resolve_token_obtain_pair_url('v1')
        self.resolve_token_refresh_url('v1')
        self.resolve_profile_list_url('v1')
        self.resolve_profile_create_url('v1', 'mytoken')
        self.resolve_profile_detail_url('v1', 1)

    def resolve_signup_url(self, version):
        r = self.resolve_by_name(
            'accounts:signup', version=version)
        self.assertEqual(r.func.cls, views.SignUpView)

    def resolve_current_user_detail_url(self, version):
        r = self.resolve_by_name(
            'accounts:current_user_detail', version=version)
        self.assertEqual(r.func.cls, views.CurrentUserDetailView)

    def resolve_token_obtain_pair_url(self, version):
        r = self.resolve_by_name(
            'accounts:token_obtain_pair', version=version)
        self.assertEqual(r.func.cls, views.TokenObtainPairView)

    def resolve_token_refresh_url(self, version):
        r = self.resolve_by_name(
            'accounts:token_refresh', version=version)
        self.assertEqual(r.func.cls, views.TokenRefreshView)

    def resolve_profile_list_url(self, version):
        r = self.resolve_by_name(
            'accounts:profile_list', version=version)
        self.assertEqual(r.func.cls, views.ProfileListView)

    def resolve_profile_create_url(self, version, token):
        r = self.resolve_by_name(
            'accounts:profile_create', version=version, token=token)
        self.assertEqual(r.func.cls, views.ProfileCreateView)

    def resolve_profile_detail_url(self, version, pk):
        r = self.resolve_by_name(
            'accounts:profile_detail', version=version, pk=pk)
        self.assertEqual(r.func.cls, views.ProfileDetailView)

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
