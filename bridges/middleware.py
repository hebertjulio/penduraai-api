from django.conf import settings

from jwt import decode as jwt_decode

from jwt import (
    InvalidAudience, InvalidSignatureError, ExpiredSignatureError,
    DecodeError)

from .models import Transaction


class LoadTransactionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        transaction = self.get_object(request)
        if transaction:
            request.transaction = transaction
        response = self.get_response(request)
        return response

    @classmethod
    def get_object(cls, request):
        token = cls.get_token(request.headers)
        if not token:
            return None
        payload = cls.get_payload(token)
        if not payload:
            return None
        try:
            obj = Transaction.objects.get(pk=payload['id'])
            return obj
        except Transaction.DoesNotExist:
            pass
        return None

    @classmethod
    def get_payload(cls, token):
        try:
            payload = jwt_decode(
                token, settings.SECRET_KEY, audience=Transaction.AUDIENCE,
                algorithms=['HS256'])
            return payload
        except (
            InvalidSignatureError, InvalidAudience,
                ExpiredSignatureError, DecodeError):
            pass
        return None

    @classmethod
    def get_token(cls, headers):
        try:
            value = headers['Transaction']
            return value
        except (KeyError, ValueError):
            return None
