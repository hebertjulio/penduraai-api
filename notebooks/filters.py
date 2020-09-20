from django_filters import rest_framework as filters

from .models import Sheet


class SheetFilterSet(filters.FilterSet):

    is_active = filters.BooleanFilter(method='is_active_filter')
    by = filters.CharFilter(method='by_filter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_active_filter(self, queryset, name, value):
        qs = queryset.filter(is_active=value)
        return qs

    def by_filter(self, queryset, name, value):  # skipcq
        user = self.request.user
        by_filter = {
            'merchant': self.by_merchant,
            'customer': self.by_customer
        }.get(value, lambda *args: Sheet.objects.none())
        queryset = by_filter(queryset, user, user.profile)
        return queryset

    @classmethod
    def by_merchant(cls, queryset, user, profile):
        where = {'customer': user}
        if not profile.is_owner:
            where.update({'profiles': profile})
        queryset = queryset.filter(**where)
        queryset = queryset.order_by('merchant__name')
        return queryset

    @classmethod
    def by_customer(cls, queryset, user, profile):
        if not profile.is_guest:
            queryset = queryset.filter(merchant=user)
            queryset = queryset.order_by('customer__name')
        return queryset

    class Meta:
        fields = [
            'by', 'is_active'
        ]
