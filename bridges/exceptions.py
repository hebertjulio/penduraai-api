from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class InvalidScopeException(APIException):

    status_code = HTTP_400_BAD_REQUEST
    default_detail = _('Transaction invalid scope.')
    default_code = 'invalid'


class InvalidUsageException(APIException):

    status_code = HTTP_400_BAD_REQUEST
    default_detail = _('Transaction invalid usage.')
    default_code = 'invalid'
