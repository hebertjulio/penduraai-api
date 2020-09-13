from django.urls import path

from .consumers import TicketConsumer


urlpatterns = [
    path('tickets/<str:ticket_id>', TicketConsumer),
]
