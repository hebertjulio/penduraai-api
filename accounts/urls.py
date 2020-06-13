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
        'current-user',
        views.CurrentUserDetailView.as_view(),
        name='current_user_detail'),
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
