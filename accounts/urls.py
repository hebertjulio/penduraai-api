from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path(
        'users',
        views.UserListView.as_view(),
        name='user_list'),
    path(
        'profiles/ticket/<str:ticket_id>/confirm',
        views.ProfileConfirmView.as_view(),
        name='profile_confirm'),
    path(
        'profiles',
        views.ProfileListView.as_view(),
        name='profile_list'),
    path(
        'profiles/<int:profile_id>',
        views.ProfileDetailView.as_view(),
        name='profile_detail'),
    path(
        'profiles/roles',
        views.ProfileRolesView.as_view(),
        name='profile_roles'),
    path(
        'profiles/<int:profile_id>/unlock',
        views.ProfileUnlockView.as_view(),
        name='profile_unlock'),
    path(
        'token-obtain-pair',
        views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token-refresh',
        views.TokenRefreshView.as_view(),
        name='token_refresh'),
    path(
        'current-profile',
        views.CurrentProfileView.as_view(),
        name='current_profile'),
    path(
        'current-user',
        views.CurrentUserView.as_view(),
        name='current_user'),
]
