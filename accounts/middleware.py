from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken

from .models import Profile


class LoadProfileMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = self.get_user_id(request)
        profile_id = self.get_profile_id(request)
        obj = None
        try:
            if profile_id is not None and user_id is not None:
                obj = Profile.objects.get(pk=profile_id, user_id=user_id)
        except Profile.DoesNotExist:
            pass
        request.profile = obj
        response = self.get_response(request)
        return response

    @classmethod
    def get_user_id(cls, request):
        auth = JWTAuthentication()
        header = auth.get_header(request)
        if header is None:
            return None
        raw_token = auth.get_raw_token(header)
        if raw_token is None:
            return None
        try:
            validated_token = auth.get_validated_token(raw_token)
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            return user_id
        except InvalidToken:
            pass
        return None

    @classmethod
    def get_profile_id(cls, request):
        headers = request.headers
        if 'Profile' not in headers:
            return None
        try:
            name, value = headers['Profile'].split()
            if name.upper() != 'PK':
                return None
            value = int(value)
            return value
        except ValueError:
            return None
