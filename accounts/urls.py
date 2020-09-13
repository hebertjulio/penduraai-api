from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path(
        'users',
        views.UserListView.as_view(),
        name='user_list'),
    path(
        'current-user',
        views.CurrentUserDetailView.as_view(),
        name='current_user_detail'),
    path(
        'profiles/ticket/<str:ticket_id>',
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
        'token-obtain-pair',
        views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token-refresh',
        views.TokenRefreshView.as_view(),
        name='token_refresh'),
]
