from django.urls import path

from . import views


app_name = 'bridges'

urlpatterns = [
    path(
        'transactions/<int:pk>',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'),
    path(
        'transactions/<int:pk>/discard',
        views.TransactionDiscardView.as_view(),
        name='transaction_discard'),
]
