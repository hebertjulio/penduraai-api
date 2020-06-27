from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class TransactionNotFound(APIException):

    status_code = HTTP_400_BAD_REQUEST
    default_detail = _('Transaction not found.')


class TransactionScopeInvalid(APIException):

    status_code = HTTP_400_BAD_REQUEST
    default_detail = _('Invalid transaction scope.')


class TransactionStatusInvalid(APIException):

    status_code = HTTP_400_BAD_REQUEST
    default_detail = _('Invalid transaction status.')


class TransactionExpired(APIException):

    status_code = HTTP_400_BAD_REQUEST
    default_detail = _('Transaction live time expired.')
