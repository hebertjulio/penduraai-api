from uuid import uuid4

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from rest_framework import serializers

from .dbdict import Transaction


class TransactionBaseSerializer(serializers.Serializer):

    token = serializers.CharField(read_only=True)

    @staticmethod
    def get_token():
        token = str(uuid4())
        token = urlsafe_base64_encode(force_bytes(token))
        return token

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class TransactionSerializer(TransactionBaseSerializer):

    scope = serializers.CharField(read_only=True)
    payload = serializers.JSONField(read_only=True)
    status = serializers.CharField(read_only=True)
    ttl = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class TransactionProfileSerializer(TransactionBaseSerializer):

    is_attendant = serializers.BooleanField(write_only=True)
    is_manager = serializers.BooleanField(write_only=True)

    def create(self, validated_data):
        request = self.context['request']
        validated_data.update({'user': request.user.id})
        token = TransactionProfileSerializer.get_token()
        transaction = Transaction(token)
        transaction.scope = Transaction.SCOPE.profile
        transaction.payload = validated_data
        transaction.save(60*30)
        return {'token': token}

    def update(self, instance, validated_data):
        raise NotImplementedError


class TransactionRecordSerializer(TransactionBaseSerializer):

    note = serializers.CharField(required=False, write_only=True)
    operation = serializers.CharField(write_only=True)

    value = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True
    )

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        profile = user.profile
        validated_data.update({'store': user.id, 'attendant': profile.id})
        token = TransactionRecordSerializer.get_token()
        transaction = Transaction(token)
        transaction.scope = Transaction.SCOPE.record
        transaction.payload = validated_data
        transaction.save(60*30)
        return {'token': token}

    def update(self, instance, validated_data):
        raise NotImplementedError


class TransactionSheetSerializer(TransactionBaseSerializer):

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        token = TransactionRecordSerializer.get_token()
        transaction = Transaction(token)
        transaction.scope = Transaction.SCOPE.sheet
        transaction.payload = {'store': user.id}
        transaction.save(60*30)
        return {'token': token}

    def update(self, instance, validated_data):
        raise NotImplementedError
