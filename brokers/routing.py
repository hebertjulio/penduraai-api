from django.urls import path

from .consumers import TransactionConsumer


routing = [
    path("transactions", TransactionConsumer),
]
