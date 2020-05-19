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
        'logged-user',
        views.LoggedUserDetailView.as_view(),
        name='logged_user_detail'),
    path(
        'logged-user/deactivate',
        views.LoggedUserDeactivateView.as_view(),
        name='logged_user_deactivate'),
    path(
        'token',
        views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token/refresh',
        views.TokenRefreshView.as_view(),
        name='token_refresh'),
]
