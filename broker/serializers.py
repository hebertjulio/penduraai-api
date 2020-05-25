import uuid
import json

from rest_framework import serializers
from model_utils import Choices

from books.serializers import RecordCreateSerializer

from .storages import Transaction


class TransactionSerializer(serializers.Serializer):

    OPERATION = Choices(
        ('record-create', RecordCreateSerializer),
    )

    transaction = serializers.UUIDField(read_only=True)
    operation = serializers.ChoiceField(choices=OPERATION, write_only=True)
    data = serializers.JSONField(write_only=True)
    channel_name = serializers.CharField(max_length=255, write_only=True)

    def validate_data(self, value):
        # translate fields
        field = {
            'creditor': 'creditor_id', 'debtor': 'debtor_id',
            'buyer': 'buyer_id', 'seller': 'seller_id',
        }
        value = {
            **{field[k]: v for k, v in value.items() if k in field.keys()},
            **{k: v for k, v in value.items() if k not in field.keys()}
        }
        return value

    def create(self, validated_data):
        transaction = str(uuid.uuid4())
        tran = Transaction(transaction)
        tran.channel_name = validated_data['channel_name']
        tran.data = json.dumps(validated_data['data'])
        return {
            'transaction': transaction
        }
