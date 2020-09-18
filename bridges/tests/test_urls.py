from django.urls import reverse, resolve

from .. import views


class TestURL:

    def test_resolve_transaction_detail_url(self):
        kwargs = {'version': 'v1', 'transaction': 'tokenhere'}
        r = self.resolve_by_name('bridges:transaction_detail', **kwargs)
        assert r.func.cls == views.TransactionDetailView  # nosec

    def test_resolve_transaction_reject_url(self):
        kwargs = {'version': 'v1', 'transaction': 'tokenhere'}
        r = self.resolve_by_name('bridges:transaction_discard', **kwargs)
        assert r.func.cls == views.TransactionDiscardView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
