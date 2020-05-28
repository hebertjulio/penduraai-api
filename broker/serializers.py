from rest_framework import serializers

from .dictdb import Transaction
from .validators import (
    TransactionCodeExistValidator, TransactionSignatureValidator)


class BaseTransactionSerializer(serializers.Serializer):

    uuid = serializers.UUIDField(write_only=True, validators=[
        TransactionCodeExistValidator(),
        TransactionSignatureValidator(),
    ])

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TransactionSerializer(BaseTransactionSerializer):

    data = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        data = validated_data['data']
        tran = Transaction()
        tran.expire = 60*30  # 30 minutes
        tran.data = data
        return {
            'uuid': tran.uuid
        }

    def update(self, instance, validated_data):
        pass

    class Meta:
        read_only_fields = [
            'uuid'
        ]
