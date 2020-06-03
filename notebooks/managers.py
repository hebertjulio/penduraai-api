from django.db.models import Manager


class CustomerManager(Manager):

    __SQL = """
        SELECT u.id AS id, u.name AS name,
            SUM(CASE WHEN r.operation='payment'
                THEN value ELSE 0 END) AS payment,
            SUM(CASE WHEN r.operation='debt'
                THEN value ELSE 0 END) AS debt
        FROM notebooks_customer AS c
        LEFT JOIN accounts_user AS u
            ON u.id = c.{groupby}_id
        LEFT JOIN notebooks_record AS r
            ON r.creditor_id = c.creditor_id
                AND r.debtor_id = c.debtor_id
        GROUP BY c.{groupby}_id
        HAVING c.{having}_id = {id}
    """

    def debtors(self, _id):
        from django.db import connection
        with connection.cursor() as cursor:
            sql = self.__SQL.format(
                groupby='debtor', having='creditor', id=_id)
            cursor.execute(sql)
            for row in cursor.fetchall():
                yield dict(zip([
                    'user_id', 'name', 'payment', 'debt'
                ], row))

    def creditors(self, _id):
        from django.db import connection
        with connection.cursor() as cursor:
            sql = self.__SQL.format(
                groupby='creditor', having='debtor', id=_id)
            cursor.execute(sql)
            for row in cursor.fetchall():
                yield dict(zip([
                    'user_id', 'name', 'payment', 'debt'
                ], row))
