from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from model_utils import Choices

from .dictdb import Transaction
from .validators import (
    TransactionCodeExistValidator, TransactionSignatureValidator)


class TransactionSerializer(serializers.Serializer):

    STATUS = Choices(
        ('awaiting', _('awaiting')),
        ('accepted', _('accepted')),
        ('rejected', _('rejected')),
    )

    id = serializers.UUIDField(read_only=True, validators=[
        TransactionCodeExistValidator(),
        TransactionSignatureValidator(),
    ])

    payload = serializers.JSONField(write_only=True)
    status = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        payload = validated_data['payload']
        tran = Transaction()
        tran.payload = payload
        tran.save(expire=60*30)  # 30 minutes
        return {
            'id': tran.id
        }

    def update(self, instance, validated_data):
        pass
