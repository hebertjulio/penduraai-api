from django.urls import path

from .consumers import RecordAwaitingAcceptConsumer


urlpatterns = [
    path(
        'records/awaiting-accept',
        RecordAwaitingAcceptConsumer
    ),
]
