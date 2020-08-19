from django.urls import path, re_path

from . import views


app_name = 'bridges'

urlpatterns = [
    re_path(
        r'^tickets/(?P<scope>(profile|sheet|record))$',
        views.TicketListView.as_view(),
        name='ticket_list'),
    path(
        'tickets/<str:token>',
        views.TicketDetailView.as_view(),
        name='ticket_detail'),
    path(
        'tickets/<str:token>/discard',
        views.TicketDiscardView.as_view(),
        name='ticket_discard'),
]
