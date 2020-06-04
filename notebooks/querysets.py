from django.db.models import QuerySet


class CustomerQuerySet(QuerySet):

    __BALANCE_QUERY = """
        SELECT
            SUM(CASE WHEN operation='payment' THEN value END) -
            SUM(CASE WHEN operation='debt' THEN value END)
        FROM notebooks_record
        WHERE creditor_id = notebooks_customer.creditor_id
        AND debtor_id = notebooks_customer.debtor_id
    """

    def creditors(self, debtor):
        qs = self.filter(debtor=debtor)
        qs = qs.extra({'balance': self.__BALANCE_QUERY})  # nosec
        return qs

    def debtors(self, creditor):
        qs = self.filter(creditor=creditor)
        qs = qs.extra({'balance': self.__BALANCE_QUERY})  # nosec
        return qs

    def balance(self, creditor, debtor):
        qs = self.filter(creditor=creditor, debtor=debtor)
        qs = qs.extra({'balance': self.__BALANCE_QUERY})  # nosec
        qs = qs.values('balance')
        if qs:
            return qs[0]['balance'] or 0
        return 0