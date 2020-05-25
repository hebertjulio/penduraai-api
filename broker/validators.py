from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .dictdb import Transaction


class IdValidator:

    def __call__(self, value):
        tran = Transaction(str(value))
        if not tran.exist():
            message = _('Id non-existent.')
            raise serializers.ValidationError(message)
