from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class BadRequest(APIException):

    status_code = HTTP_400_BAD_REQUEST

    def __init__(self, detail):
        super().__init__(detail=detail, code='bad_request')
