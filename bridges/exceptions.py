from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class TokenDecodeException(APIException):

    status_code = HTTP_400_BAD_REQUEST
    default_code = 'invalid'

    def __init__(self, detail):
        super().__init__(detail=_(detail))
