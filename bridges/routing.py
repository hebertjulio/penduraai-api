from django.urls import path

from .consumers import TicketConsumer


urlpatterns = [
    path('tickets/<str:token>', TicketConsumer),
]
