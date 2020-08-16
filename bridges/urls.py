from django.urls import path

from . import views


app_name = 'bridges'

urlpatterns = [
    path(
        'transactions',
        views.TransactionListView.as_view(),
        name='transaction_list'),
    path(
        'transactions/<int:transaction_id>',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'),
    path(
        'transactions/<int:transaction_id>/discard',
        views.TransactionDiscardView.as_view(),
        name='transaction_discard'),
]
