from django.urls import path, re_path

from . import views


app_name = 'bridges'

urlpatterns = [
    re_path(
        r'^tickets/(?P<scope>(profile|sheet|record))$',
        views.TicketListView.as_view(),
        name='ticket_list'),
    path(
        'tickets/<str:ticket_id>',
        views.TicketDetailView.as_view(),
        name='ticket_detail'),
    path(
        'tickets/<str:ticket_id>/discard',
        views.TicketDiscardView.as_view(),
        name='ticket_discard'),
]
