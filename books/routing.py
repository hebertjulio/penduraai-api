from django.urls import path

from .consumers import RecordTransactionConsumer


routing = [
    path('record-transaction', RecordTransactionConsumer),
]
