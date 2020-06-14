from rest_framework import serializers

from .models import User, Profile


class UserRelatedField(serializers.RelatedField):

    def get_queryset(self):
        if self.read_only:
            return None
        qs = User.objects.all()
        return qs

    def to_internal_value(self, data):
        if isinstance(data, User):
            return data
        try:
            qs = self.get_queryset()
            obj = qs.get(pk=data)
            return obj
        except User.DoesNotExist:
            pass
        return data

    def to_representation(self, value):
        data = {
            'id': value.id,
            'name': value.name
        }
        return data


class ProfileRelatedField(serializers.RelatedField):

    def get_queryset(self):
        if self.read_only:
            return None
        qs = Profile.objects.all()
        return qs

    def to_internal_value(self, data):
        if isinstance(data, Profile):
            return data
        try:
            qs = self.get_queryset()
            obj = qs.get(pk=data)
            return obj
        except Profile.DoesNotExist:
            pass
        return data

    def to_representation(self, value):
        data = {
            'id': value.id,
            'name': value.name
        }
        return data
