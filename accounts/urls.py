from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path(
        'signup',
        views.SignUpView.as_view(),
        name='signup'),
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
        'profiles/transaction/<int:pk>',
        views.ProfileCreateView.as_view(),
        name='profile_create'),
    path(
        'profiles/request',
        views.ProfileRequestView.as_view(),
        name='profile_request'),
    path(
        'token-obtain-pair',
        views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token-refresh',
        views.TokenRefreshView.as_view(),
        name='token_refresh'),
]
