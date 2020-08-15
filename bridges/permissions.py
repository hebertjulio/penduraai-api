from django.conf import settings

from rest_framework.permissions import BasePermission

from jwt import decode as jwt_decode
from jwt import (
    InvalidAudience, InvalidSignatureError, ExpiredSignatureError,
    DecodeError)

from .models import Transaction


class HasTransactionToken(BasePermission):

    AUTHORIZATION = 'Authorization'

    @classmethod
    def get_token(cls, headers):
        if cls.AUTHORIZATION in headers:
            try:
                key, value = headers[cls.AUTHORIZATION].split(' ')
                return value
            except ValueError:
                pass
        return None

    @classmethod
    def get_payload(cls, token):
        try:
            payload = jwt_decode(
                token, settings.SECRET_KEY, audience='transaction',
                algorithms=['HS256'])
            return payload
        except InvalidSignatureError:
            pass
        except InvalidAudience:
            pass
        except ExpiredSignatureError:
            pass
        except DecodeError:
            pass
        return None

    def has_permission(self, request, view):
        token = self.get_token(request.headers)
        if token is not None:
            payload = self.get_payload(token)
            if payload:
                transaction = view.get_object()
                return bool(
                    isinstance(transaction, Transaction)
                    and transaction.id == payload['id'])
        return False
