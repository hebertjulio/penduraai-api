from rest_framework import serializers

from .dictdb import Transaction
from .validators import (
    TransactionCodeExistValidator, TransactionSignatureValidator)


class TransactionSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only=True, validators=[
        TransactionCodeExistValidator(),
        TransactionSignatureValidator(),
    ])

    payload = serializers.JSONField()
    status = serializers.ChoiceField(choices=Transaction.STATUS)

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
