from django.db.models import QuerySet, Sum, Case, When, F, DecimalField, Q


class SheetQuerySet(QuerySet):

    balance_calc = F('credit_sum') - F('debt_sum')

    credit_sum = Sum(Case(When(
        Q(sheetrecords__operation='credit') &
        Q(sheetrecords__is_active=False),
        then=F('sheetrecords__value')),
        default=0, output_field=DecimalField())
    )

    debt_sum = Sum(Case(When(
        Q(sheetrecords__operation='debt') &
        Q(sheetrecords__is_active=False),
        then=F('sheetrecords__value')),
        default=0, output_field=DecimalField())
    )

    def balance_list_by_store(self, user, profile):
        where = {'customer': user}
        if not profile.is_owner:
            where.update({'sheetbuyers__profile': profile})
        qs = self.select_related('store', 'record')
        qs = qs.annotate(
            user_id=F('store__id'), user_name=F('store__name'),
            credit_sum=self.credit_sum, debt_sum=self.debt_sum,
            balance=self.balance_calc, sheet_id=F('id'))
        qs = qs.values('user_id', 'user_name', 'balance', 'sheet_id')
        qs = qs.filter(**where)
        qs = qs.order_by('user_name')
        return qs

    def balance_list_by_customer(self, user, profile):
        where = {'store': user}
        if not profile.is_owner and not profile.is_manager:
            where.update({'sheetbuyers__profile': profile})
        qs = self.select_related('customer', 'record')
        qs = qs.annotate(
            user_id=F('customer__id'), user_name=F('customer__name'),
            credit_sum=self.credit_sum, debt_sum=self.debt_sum,
            balance=self.balance_calc, sheet_id=F('id'))
        qs = qs.values('user_id', 'user_name', 'balance', 'sheet_id')
        qs = qs.filter(**where)
        qs = qs.order_by('user_name')
        return qs
