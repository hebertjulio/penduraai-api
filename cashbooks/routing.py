from django.urls import path

from .consumers import RecordAwaitingAcceptConsumer


routings = [
    path(
        'records/awaiting-accept',
        RecordAwaitingAcceptConsumer
    ),
]
