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
        'users/update',
        views.UserUpdateView.as_view(),
        name='user_update'),
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
        'profiles/pin/<int:pin>',
        views.ProfilePinView.as_view(),
        name='profile_pin'),
    path(
        'token-obtain-pair',
        views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token-refresh',
        views.TokenRefreshView.as_view(),
        name='token_refresh'),
]
