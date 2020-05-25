import uuid
import json

from rest_framework import serializers
from model_utils import Choices

from books.serializers import RecordCreateSerializer

from .storages import Transaction
from .services import translate_fk_names


class TransactionSerializer(serializers.Serializer):

    OPERATION = Choices(
        ('record-create', RecordCreateSerializer),
    )

    transaction = serializers.UUIDField(read_only=True)
    operation = serializers.ChoiceField(choices=OPERATION, write_only=True)
    data = serializers.JSONField(write_only=True)
    channel_name = serializers.CharField(max_length=255, write_only=True)

    def create(self, validated_data):
        transaction = str(uuid.uuid4())
        tran = Transaction(transaction)
        tran.channel_name = validated_data['channel_name']
        data = translate_fk_names(validated_data['data'])
        tran.data = json.dumps(data)
        return {
            'transaction': transaction
        }

    def update(self, instance, validated_data):
        pass
