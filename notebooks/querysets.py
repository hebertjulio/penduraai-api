from django.db.models import QuerySet, Sum, Case, When, F, DecimalField, Q


class SheetQuerySet(QuerySet):

    balance_calc = F('credit_sum') - F('debt_sum')

    credit_sum = Sum(Case(When(
        Q(sheetrecords__operation='credit') &
        Q(sheetrecords__is_active=True),
        then=F('sheetrecords__value')),
        default=0, output_field=DecimalField())
    )

    debt_sum = Sum(Case(When(
        Q(sheetrecords__operation='debt') &
        Q(sheetrecords__is_active=True),
        then=F('sheetrecords__value')),
        default=0, output_field=DecimalField())
    )

    def balances(self):
        qs = self.select_related('merchant', 'customer')
        qs = qs.annotate(
            credit_sum=self.credit_sum, debt_sum=self.debt_sum,
            balance=self.balance_calc)
        return qs
