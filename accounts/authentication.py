from rest_framework.exceptions import NotAcceptable, AuthenticationFailed

from rest_framework_simplejwt import authentication

from .models import Profile


class JWTAuthentication(authentication.JWTAuthentication):

    def authenticate(self, request):
        authenticate = super().authenticate(request)
        if not authenticate:
            return None
        user, validated_token = authenticate
        profile = None
        pk = self.get_PK(request.headers)
        if pk is not None:
            profile = self.get_profile(user, pk)
        user.profile = profile
        return user, validated_token

    @classmethod
    def get_PK(cls, headers):
        if 'Profile' not in headers:
            return None
        values = headers['Profile'].split()
        if len(values) != 2:
            raise NotAcceptable
        name, value = values
        if name.upper() != 'PK':
            raise NotAcceptable
        try:
            value = int(value)
            return value
        except ValueError:
            return None

    @classmethod
    def get_profile(cls, user, pk):
        try:
            profile = user.userprofiles.get(pk=pk, is_active=True)
            return profile
        except Profile.DoesNotExist:
            raise AuthenticationFailed
