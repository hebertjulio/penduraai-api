from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path(
        'users',
        views.UserListView.as_view(),
        name='user_list'),
    path(
        'users/<int:pk>',
        views.UserDetailView.as_view(),
        name='user_detail'),
    path(
        'users/change',
        views.UserChangeView.as_view(),
        name='user_change'),
    path(
        'users/deactivate',
        views.UserDeactivateView.as_view(),
        name='user_deactivate'),
    path(
        'profiles',
        views.ProfileListView.as_view(),
        name='profile_list'),
    path(
        'profiles/<int:pk>',
        views.ProfileDetailView.as_view(),
        name='profile_detail'),
    path(
        'whitelists',
        views.WhitelistListView.as_view(),
        name='whitelist_list'),
    path(
        'whitelists/<int:pk>',
        views.WhitelistDetailView.as_view(),
        name='whitelist_detail'),
    path(
        'token-obtain-pair',
        views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token-refresh',
        views.TokenRefreshView.as_view(),
        name='token_refresh'),
]
