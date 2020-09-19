from django_filters import rest_framework as filters

from .models import Sheet


class SheetFilterSet(filters.FilterSet):

    by = filters.CharFilter(method='filter_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_by(self, queryset, name, value):  # skipcq
        user = self.request.user
        profile = self.request.user.profile
        by = {
            'merchant': self.filter_by_merchant,
            'customer': self.filter_by_customer
        }
        return by.get(value, lambda *args: Sheet.objects.none())(
            queryset, user, profile
        )

    @classmethod
    def filter_by_merchant(cls, queryset, user, profile):
        where = {'customer': user}
        if not profile.is_owner:
            where.update({'profiles': profile})
        queryset = queryset.filter(**where)
        queryset = queryset.order_by('merchant__name')
        return queryset

    @classmethod
    def filter_by_customer(cls, queryset, user, profile):
        if not profile.is_guest:
            queryset = queryset.filter(merchant=user)
            queryset = queryset.order_by('customer__name')
        return queryset

    class Meta:
        fields = [
            'by'
        ]
