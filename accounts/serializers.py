from django.db import transaction

from rest_framework import serializers

from .models import User, Profile


class SignUpSerializer(serializers.ModelSerializer):

    pin = serializers.RegexField(regex=Profile.PIN_REGEX, write_only=True)

    @transaction.atomic
    def create(self, validated_data):
        pin = validated_data.pop('pin')
        user = User(**validated_data)
        user.is_active = True
        user.set_password(validated_data['password'])
        user.save()
        # create owner profile
        profile = Profile(**{
            'name': user.name, 'pin': pin, 'user': user,
            'is_owner': True
        })
        profile.save()
        return user

    def update(self, instance, validated_data):
        pass

    class Meta:
        model = User
        exclude = [
            'user_permissions', 'groups', 'is_superuser',
            'is_staff'
        ]
        read_only_fields = [
            'id', 'is_active', 'last_login', 'created',
            'modified'
        ]


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        user = instance
        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
        user = super().update(user, validated_data)
        return user

    class Meta:
        model = User
        exclude = [
            'user_permissions', 'groups', 'is_superuser',
            'is_staff'
        ]
        read_only_fields = [
            'id', 'is_active', 'last_login', 'created',
            'modified'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = [
            'is_owner'
        ]
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }
