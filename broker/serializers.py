from rest_framework import serializers

from .dictdb import Transaction
from .validators import (
    TransactionCodeExistValidator, TransactionSignatureValidator)


class BaseTransactionSerializer(serializers.Serializer):

    transaction = serializers.UUIDField(write_only=True, validators=[
        TransactionCodeExistValidator(),
        TransactionSignatureValidator(),
    ])

    def update(self, instance, validated_data):
        pass


class TransactionSerializer(BaseTransactionSerializer):

    data = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        data = validated_data['data']
        tran = Transaction()
        tran.expire = 60*10  # 10 minutes
        tran.data = data
        return {
            'transaction': tran.code
        }

    def update(self, instance, validated_data):
        pass

    class Meta:
        read_only_fields = [
            'transaction'
        ]
