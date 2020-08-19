from django.utils.translation import gettext_lazy as _


class TokenEncodeException(Exception):

    def __init__(self):
        message = _('Token is invalid.')
        super().__init__(message)
