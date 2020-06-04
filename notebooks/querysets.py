from django.db.models import QuerySet


class CustomerQuerySet(QuerySet):

    __BALANCE_SQL = """
        SELECT
            SUM(CASE WHEN operation='payment' THEN value ELSE 0.0 END) -
            SUM(CASE WHEN operation='debt' THEN value ELSE 0.0 END)
        FROM notebooks_record
        WHERE creditor_id = notebooks_customer.creditor_id
        AND debtor_id = notebooks_customer.debtor_id
    """

    def creditors(self, debtor):
        qs = self.filter(debtor=debtor)
        qs = qs.extra({'balance': self.__BALANCE_SQL})  # nosec
        return qs

    def debtors(self, creditor):
        qs = self.filter(creditor=creditor)
        qs = qs.extra({'balance': self.__BALANCE_SQL})  # nosec
        return qs

    def balance(self, creditor, debtor):
        qs = self.filter(creditor=creditor, debtor=debtor)
        qs = qs.extra({'balance': self.__BALANCE_SQL})  # nosec
        qs = qs.values('balance')
        if qs:
            return qs[0]['balance'] or 0.0
        return 0.0
