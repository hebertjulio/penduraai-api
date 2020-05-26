import json

from rest_framework import serializers

from .dictdb import Transaction


class TransactionSerializer(serializers.Serializer):

    transaction = serializers.UUIDField(read_only=True)
    data = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        data = validated_data['data']
        tran = Transaction()
        tran.data = json.dumps(data)
        return {
            'transaction': tran.code
        }

    def update(self, instance, validated_data):
        pass
