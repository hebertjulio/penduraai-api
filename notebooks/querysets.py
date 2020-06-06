from django.db.models import (QuerySet, Sum, Case, When, F, DecimalField)


class CustomerQuerySet(QuerySet):

    balance = F('payment_sum') - F('debt_sum')

    payment_sum = Sum(Case(When(
        customer_record__operation='payment',
        then=F('customer_record__value')),
        default=0, output_field=DecimalField())
    )

    debt_sum = Sum(Case(When(
        customer_record__operation='debt',
        then=F('customer_record__value')),
        default=0, output_field=DecimalField())
    )

    def creditors(self, debtor):
        qs = self.filter(
            debtor=debtor, customer_record__strikethrough=False
        )
        qs = qs.annotate(
            payment_sum=self.payment_sum,
            debt_sum=self.debt_sum,
            balance=self.balance
        )
        return qs

    def debtors(self, creditor):
        qs = self.filter(
            creditor=creditor, customer_record__strikethrough=False
        )
        qs = qs.annotate(
            payment_sum=self.payment_sum,
            debt_sum=self.debt_sum,
            balance=self.balance
        )
        return qs
