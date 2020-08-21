from rest_framework import serializers

from .db import Ticket


class TicketSerializer(serializers.Serializer):

    scope = serializers.CharField(required=True)
    expire = serializers.IntegerField(required=True)
    data = serializers.JSONField(binary=True, required=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        ticket = Ticket(validated_data['scope'])
        ticket.data = validated_data['data']
        ticket.expire = validated_data['expire']
        return ticket
