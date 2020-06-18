from rest_framework.exceptions import APIException


class StatusNotAllowedException(APIException):

    status_code = 403
    default_detail = 'Transaction status not allowed.'
    default_code = 'bad_request'


class ScopeNotAllowedException(APIException):

    status_code = 403
    default_detail = 'Transaction scope not allowed.'
    default_code = 'bad_request'


class TransactionNotFoundException(APIException):

    status_code = 404
    default_detail = 'Transaction not found.'
    default_code = 'not_found'
