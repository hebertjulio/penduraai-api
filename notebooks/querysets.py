from django.db.models import QuerySet, Sum, Case, When, F, DecimalField, Q


class SheetQuerySet(QuerySet):

    balance_calc = F('credit_sum') - F('debt_sum')

    credit_sum = Sum(Case(When(
        Q(records__operation='credit') &
        Q(records__deleted=False),
        then=F('records__value')),
        default=0, output_field=DecimalField())
    )

    debt_sum = Sum(Case(When(
        Q(records__operation='debt') &
        Q(records__deleted=False),
        then=F('records__value')),
        default=0, output_field=DecimalField())
    )

    def store_list(self, customer):
        qs = self.filter(customer=customer)
        qs = qs.annotate(
            user_id=F('store__id'), user_name=F('store__name'),
            credit_sum=self.credit_sum, debt_sum=self.debt_sum,
            balance=self.balance_calc
        )
        qs = qs.values('user_id', 'user_name', 'balance')
        qs = qs.order_by('user_name')
        return qs

    def customer_list(self, store):
        qs = self.filter(store=store)
        qs = qs.annotate(
            user_id=F('customer__id'), user_name=F('customer__name'),
            credit_sum=self.credit_sum, debt_sum=self.debt_sum,
            balance=self.balance_calc
        )
        qs = qs.values('user_id', 'user_name', 'balance')
        qs = qs.order_by('user_name')
        return qs
