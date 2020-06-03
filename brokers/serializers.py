import uuid

from rest_framework import serializers

from .dictdb import Transaction


class TransactionSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    payload = serializers.JSONField(binary=True)
    status = serializers.ChoiceField(
        choices=Transaction.STATUS, read_only=True)

    def create(self, validated_data):
        request = self.context['request']
        tran = Transaction(str(uuid.uuid4()))
        tran.payload = validated_data['payload']
        tran.payload.update({'creditor': request.user.id})
        tran.save(60*30)  # 30 minutes
        return tran.data

    def update(self, instance, validated_data):
        pass
