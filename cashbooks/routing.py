from django.urls import path

from .consumers import RecordAwaitingAcceptConsumer


routing = [
    path(
        'records/awaiting-accept',
        RecordAwaitingAcceptConsumer
    ),
]
