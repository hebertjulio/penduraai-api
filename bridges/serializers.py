from rest_framework import serializers

from .db import Ticket


class TicketSerializer(serializers.Serializer):

    scope = serializers.CharField(required=True)
    expire = serializers.IntegerField(required=True, write_only=True)
    data = serializers.JSONField(binary=True, required=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        expire = validated_data['expire'] * 60
        ticket = Ticket(validated_data['scope'])
        ticket.data = validated_data['data']
        ticket.persist(expire)
        return ticket
