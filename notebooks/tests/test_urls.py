from django.urls import reverse, resolve

from .. import views


class TestURL:

    def test_resolve_record_request_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:record_request', **kwargs)
        assert r.func.cls == views.RecordRequestView  # nosec

    def test_resolve_record_list_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:record_list', **kwargs)
        assert r.func.cls == views.RecordListView  # nosec

    def test_resolve_record_detail_url(self):
        kwargs = {'version': 'v1', 'pk': 1}
        r = self.resolve_by_name('notebooks:record_detail', **kwargs)
        assert r.func.cls == views.RecordDetailView  # nosec

    def test_resolve_sheet_request_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:sheet_request', **kwargs)
        assert r.func.cls == views.SheetRequestView  # nosec

    def test_resolve_sheet_list_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:sheet_list', **kwargs)
        assert r.func.cls == views.SheetListView  # nosec

    def test_resolve_sheet_detail_url(self):
        kwargs = {'version': 'v1', 'pk': 1}
        r = self.resolve_by_name('notebooks:sheet_detail', **kwargs)
        assert r.func.cls == views.SheetDetailView  # nosec

    def test_resolve_sheet_profile_manage_url(self):
        kwargs = {'version': 'v1', 'pk': 1, 'profile_id': 1}
        r = self.resolve_by_name('notebooks:sheet_profile_manage', **kwargs)
        assert r.func.cls == views.SheetProfileManageView  # nosec

    def test_resolve_balance_list_by_merchant_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:balance_list_by_merchant', **kwargs)
        assert r.func.cls == views.BalanceListByMerchantView  # nosec

    def test_resolve_balance_list_by_customer_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:balance_list_by_customer', **kwargs)
        assert r.func.cls == views.BalanceListByCustomerView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
