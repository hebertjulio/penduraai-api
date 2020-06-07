from django.db.models import QuerySet, Sum, Case, When, F, DecimalField, Q


class CustomerQuerySet(QuerySet):

    balance_calc = F('payment_sum') - F('debt_sum')

    payment_sum = Sum(Case(When(
        Q(customer_record__operation='payment') &
        Q(customer_record__strikethrough=False),
        then=F('customer_record__value')),
        default=0, output_field=DecimalField())
    )

    debt_sum = Sum(Case(When(
        Q(customer_record__operation='debt') &
        Q(customer_record__strikethrough=False),
        then=F('customer_record__value')),
        default=0, output_field=DecimalField())
    )

    def creditors(self, debtor):
        qs = self.filter(debtor=debtor)
        qs = qs.annotate(
            user_id=F('creditor__id'), user_name=F('creditor__name'),
            payment_sum=self.payment_sum, debt_sum=self.debt_sum,
            balance=self.balance_calc
        )
        qs = qs.values('user_id', 'user_name', 'balance')
        qs = qs.order_by('user_name')
        return qs

    def debtors(self, creditor):
        qs = self.filter(creditor=creditor)
        qs = qs.annotate(
            user_id=F('debtor__id'), user_name=F('debtor__name'),
            payment_sum=self.payment_sum, debt_sum=self.debt_sum,
            balance=self.balance_calc
        )
        qs = qs.values('user_id', 'user_name', 'balance')
        qs = qs.order_by('user_name')
        return qs
