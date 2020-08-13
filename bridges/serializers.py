from rest_framework import serializers

from .models import Transaction


class TransactionWriteSerializer(serializers.ModelSerializer):

    data = serializers.JSONField(binary=True, required=True)

    class Meta:
        model = Transaction
        exclude = [
            'scope', 'expire_at'
        ]


class TransactionReadSerializer(serializers.ModelSerializer):

    token = serializers.CharField(read_only=True)
    expired = serializers.BooleanField(read_only=True)
    data = serializers.JSONField(read_only=True, source='data_as_dict')

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', [])
        super().__init__(*args, **kwargs)
        for field in exclude:
            self.fields.pop(field)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = [
            f for f in Transaction.get_fields()
        ]
