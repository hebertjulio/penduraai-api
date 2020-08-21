from uuid import uuid4

from rest_framework import serializers

from .db import Ticket


class TicketSerializer(serializers.Serializer):

    exp = serializers.IntegerField(required=True, write_only=True)
    scope = serializers.CharField(required=True)
    data = serializers.JSONField(binary=True, required=True)
    token = serializers.CharField(read_only=True)
    ttl = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        key = str(uuid4())
        expire = validated_data['exp'] * 60
        ticket = Ticket(key, validated_data['scope'], expire=expire)
        ticket.data = validated_data['data']
        return ticket
