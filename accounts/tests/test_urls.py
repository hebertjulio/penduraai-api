from django.urls import reverse, resolve

from .. import views


class TestURL:

    def test_resolve_user_list_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:user_list', **kwargs)
        assert r.func.cls == views.UserListView  # nosec

    def test_resolve_current_user_detail_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:current_user_detail', **kwargs)
        assert r.func.cls == views.CurrentUserDetailView  # nosec

    def test_resolve_token_obtain_pair_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:token_obtain_pair', **kwargs)
        assert r.func.cls == views.TokenObtainPairView  # nosec

    def test_resolve_token_refresh_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:token_refresh', **kwargs)
        assert r.func.cls == views.TokenRefreshView  # nosec

    def resolve_profile_list_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:profile_list', **kwargs)
        assert r.func.cls == views.ProfileListView  # nosec

    def test_resolve_profile_detail_url(self):
        kwargs = {'version': 'v1', 'profile_id': 1}
        r = self.resolve_by_name('accounts:profile_detail', **kwargs)
        assert r.func.cls == views.ProfileDetailView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
