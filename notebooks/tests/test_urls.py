from django.urls import reverse, resolve

from .. import views


class TestURL:

    def test_resolve_record_list_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:record_list', **kwargs)
        assert r.func.cls == views.RecordListView  # nosec

    def test_resolve_record_detail_url(self):
        kwargs = {'version': 'v1', 'record_id': 1}
        r = self.resolve_by_name('notebooks:record_detail', **kwargs)
        assert r.func.cls == views.RecordDetailView  # nosec

    def test_resolve_sheet_list_url(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:sheet_list', **kwargs)
        assert r.func.cls == views.SheetListView  # nosec

    def test_resolve_sheet_detail_url(self):
        kwargs = {'version': 'v1', 'sheet_id': 1}
        r = self.resolve_by_name('notebooks:sheet_detail', **kwargs)
        assert r.func.cls == views.SheetDetailView  # nosec

    def test_resolve_sheet_buyer_url(self):
        kwargs = {'version': 'v1', 'sheet_id': 1, 'profile_id': 1}
        r = self.resolve_by_name('notebooks:sheet_buyer', **kwargs)
        assert r.func.cls == views.SheetBuyerView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
