from django.test import TestCase
from django.urls import reverse, resolve

from .. import views


class UrlsTestCase(TestCase):

    def test_resolve_transaction_record_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('bridges:transaction_record', **kwargs)
        self.assertEqual(r.func.cls, views.TransactionRecordView)

    def test_resolve_transaction_sheet_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('bridges:transaction_sheet', **kwargs)
        self.assertEqual(r.func.cls, views.TransactionSheetView)

    def test_resolve_transaction_profile_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('bridges:transaction_profile', **kwargs)
        self.assertEqual(r.func.cls, views.TransactionProfileView)

    def test_resolve_transaction_detail_url(self):
        kwargs = {'version': 'v1', 'token': 'mytoken'}
        r = self.resolve_by_name('bridges:transaction_detail', **kwargs)
        self.assertEqual(r.func.cls, views.TransactionDetailView)

    def test_resolve_transaction_reject_url(self):
        kwargs = {'version': 'v1', 'token': 'mytoken'}
        r = self.resolve_by_name('bridges:transaction_reject', **kwargs)
        self.assertEqual(r.func.cls, views.TransactionRejectView)

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
