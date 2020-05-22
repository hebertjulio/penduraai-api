from django.urls import path

from .consumers import RecordAwaitingAcceptConsumer


paths = [
    path(
        'records/awaiting-accept',
        RecordAwaitingAcceptConsumer
    ),
]
