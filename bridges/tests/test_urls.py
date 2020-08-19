from django.urls import reverse, resolve

from .. import views


class TestURL:

    def test_resolve_ticket_list_url(self):
        kwargs = {'version': 'v1', 'scope': 'profile'}
        r = self.resolve_by_name('bridges:ticket_list', **kwargs)
        assert r.func.cls == views.TicketListView  # nosec
        kwargs = {'version': 'v1', 'scope': 'sheet'}
        r = self.resolve_by_name('bridges:ticket_list', **kwargs)
        assert r.func.cls == views.TicketListView  # nosec
        kwargs = {'version': 'v1', 'scope': 'record'}
        r = self.resolve_by_name('bridges:ticket_list', **kwargs)
        assert r.func.cls == views.TicketListView  # nosec

    def test_resolve_ticket_detail_url(self):
        kwargs = {'version': 'v1', 'token': 'tokenhere'}
        r = self.resolve_by_name('bridges:ticket_detail', **kwargs)
        assert r.func.cls == views.TicketDetailView  # nosec

    def test_resolve_ticket_reject_url(self):
        kwargs = {'version': 'v1', 'token': 'tokenhere'}
        r = self.resolve_by_name('bridges:ticket_discard', **kwargs)
        assert r.func.cls == views.TicketDiscardView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
