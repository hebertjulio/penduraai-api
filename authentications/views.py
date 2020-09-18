from rest_framework_api_key.permissions import HasAPIKey

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)


class LoginView(TokenObtainPairView):

    permission_classes = [
        HasAPIKey
    ]


class LoginRefreshView(TokenRefreshView):

    permission_classes = [
        HasAPIKey
    ]
