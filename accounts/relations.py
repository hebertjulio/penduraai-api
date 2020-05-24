from rest_framework import serializers

from .models import User, Profile
from .validators import CreditorAccountable, DebtorAccountable


class CreditorField(serializers.PrimaryKeyRelatedField):

    queryset = User.objects.filter(is_active=True)


class SellerField(serializers.PrimaryKeyRelatedField):

    queryset = Profile.objects.all()
    validators = [
        CreditorAccountable()
    ]


class BuyerField(serializers.PrimaryKeyRelatedField):

    queryset = Profile.objects.all()
    validators = [
        DebtorAccountable()
    ]
