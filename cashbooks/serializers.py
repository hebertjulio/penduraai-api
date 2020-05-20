from rest_framework import serializers

from accounts.fields import ProfileField

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    requester = ProfileField()
    signature = ProfileField()

    debtor = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = '__all__'
