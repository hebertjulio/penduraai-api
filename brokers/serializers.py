from rest_framework import serializers

from .dictdb import Transaction


class TransactionSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    payload = serializers.JSONField(binary=True)
    status = serializers.ChoiceField(
        choices=Transaction.STATUS, read_only=True)

    def create(self, validated_data):
        payload = validated_data['payload']
        tran = Transaction()
        tran.payload = payload
        tran.expire = 60*30  # 30 minutes
        return {
            'id': tran.id, 'payload': tran.payload,
            'status': tran.status,
        }

    def update(self, instance, validated_data):
        pass
