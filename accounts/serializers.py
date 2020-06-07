from django.db.transaction import atomic

from rest_framework import serializers

from .models import User, Profile


class UserCreateSerializer(serializers.ModelSerializer):

    pin = serializers.RegexField(regex=r'\d{4}', write_only=True)

    @atomic
    def create(self, validated_data):
        pin = validated_data.pop('pin')
        user = User(**validated_data)
        user.is_active = True
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile(**{
            'name': user.name, 'pin': pin, 'role': Profile.ROLE.owner,
            'accountable': user})
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


class UserUpdateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    @atomic
    def update(self, instance, validated_data):
        user = instance
        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
        if 'name' in validated_data:
            try:
                profile = user.accountable.get(role=Profile.ROLE.owner)
                profile.name = validated_data['name']
                profile.save()
            except Profile.DoesNotExist:
                pass
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


class UserReadSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = User
        exclude = [
            'user_permissions', 'groups', 'is_superuser',
            'is_staff', 'password'
        ]
        read_only_fields = [
            f for f in User._meta.get_fields()
        ]


class ProfileSerializer(serializers.ModelSerializer):

    accountable = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileAuthenticateSerializer(serializers.Serializer):

    accountable = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
