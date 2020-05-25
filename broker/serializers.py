import uuid
import json

from rest_framework import serializers

from .dictdb import Transaction
from .services import translate_fk_names


class TransactionSerializer(serializers.Serializer):

    transaction = serializers.UUIDField(read_only=True)
    data = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        tran = Transaction(code=str(uuid.uuid4()))
        data = translate_fk_names(validated_data['data'])
        tran.data = json.dumps(data)
        tran.save()
        return {
            'transaction': tran.code
        }

    def update(self, instance, validated_data):
        pass
