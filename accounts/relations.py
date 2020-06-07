from rest_framework.serializers import RelatedField

from .models import Profile


class SellerRelatedField(RelatedField):

    queryset = Profile.objects.filter(accountable__is_active=True)

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        qs = self.get_queryset()
        obj = qs.get(pk=data)
        return obj
