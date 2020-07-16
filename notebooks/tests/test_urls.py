from django.urls import reverse, resolve

from .. import views


class TestURL:

    def test_resolve_record_request_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:record_request', **kwargs)
        assert r.func.cls == views.RecordRequestView  # nosec

    def test_resolve_record_create_url(self):
        kwargs = {'version': 'v1', 'transaction_id': 1}
        r = self.resolve_by_name('notebooks:record_create', **kwargs)
        assert r.func.cls == views.RecordCreateView  # nosec

    def test_resolve_record_list_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:record_list', **kwargs)
        assert r.func.cls == views.RecordListView  # nosec

    def test_resolve_record_detail_url(self):
        kwargs = {'version': 'v1', 'record_id': 1}
        r = self.resolve_by_name('notebooks:record_detail', **kwargs)
        assert r.func.cls == views.RecordDetailView  # nosec

    def test_resolve_sheet_request_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:sheet_request', **kwargs)
        assert r.func.cls == views.SheetRequestView  # nosec

    def test_resolve_sheet_create_url(self):
        kwargs = {'version': 'v1', 'transaction_id': 1}
        r = self.resolve_by_name('notebooks:sheet_create', **kwargs)
        assert r.func.cls == views.SheetCreateView  # nosec

    def test_resolve_sheet_detail_url(self):
        kwargs = {'version': 'v1', 'sheet_id': 1}
        r = self.resolve_by_name('notebooks:sheet_detail', **kwargs)
        assert r.func.cls == views.SheetDetailView  # nosec

    def test_resolve_sheet_buyer_url(self):
        kwargs = {'version': 'v1', 'sheet_id': 1, 'profile_id': 1}
        r = self.resolve_by_name('notebooks:sheet_buyer', **kwargs)
        assert r.func.cls == views.SheetBuyerView  # nosec

    def test_resolve_sheet_list_url(self):
        kwargs = {'version': 'v1', 'by': 'merchant'}
        r = self.resolve_by_name('notebooks:sheet_list', **kwargs)
        assert r.func.cls == views.SheetListView  # nosec
        kwargs = {'version': 'v1', 'by': 'customer'}
        r = self.resolve_by_name('notebooks:sheet_list', **kwargs)
        assert r.func.cls == views.SheetListView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
