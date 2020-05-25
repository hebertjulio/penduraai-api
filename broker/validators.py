from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .dictdb import Storage


class IdValidator:

    def __call__(self, value):
        stg = Storage(str(value))
        if not stg.exist():
            message = _('Id non-existent.')
            raise serializers.ValidationError(message)
