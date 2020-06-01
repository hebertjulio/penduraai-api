from django.urls import path

from .consumers import TransactionConsumer


routing = [
    path('transactions/<str:pk>', TransactionConsumer),
]
