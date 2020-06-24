from django.test import TestCase
from django.urls import reverse, resolve

from .. import views


class UrlsTestCase(TestCase):

    def test_resolve_transaction_detail_url(self):
        kwargs = {'version': 'v1', 'pk': 1}
        r = self.resolve_by_name('bridges:transaction_detail', **kwargs)
        self.assertEqual(r.func.cls, views.TransactionDetailView)

    def test_resolve_transaction_reject_url(self):
        kwargs = {'version': 'v1', 'pk': 1}
        r = self.resolve_by_name('bridges:transaction_discard', **kwargs)
        self.assertEqual(r.func.cls, views.TransactionDiscardView)

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
