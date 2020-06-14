from rest_framework import serializers

from .models import Sheet


class SheetRelatedField(serializers.RelatedField):

    def get_queryset(self):
        if self.read_only:
            return None
        qs = Sheet.objects.all()
        return qs

    def to_internal_value(self, data):
        if isinstance(data, Sheet):
            return data
        try:
            qs = self.get_queryset()
            obj = qs.get(pk=data)
            return obj
        except Sheet.DoesNotExist:
            pass
        return data

    def to_representation(self, value):
        data = {
            'id': value.id,
            'store': {
                'id': value.store.id,
                'name': value.store.name,
            },
            'customer': {
                'id': value.customer.id,
                'name': value.customer.name,
            },
        }
        return data