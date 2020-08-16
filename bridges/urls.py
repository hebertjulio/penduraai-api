from django.urls import path, re_path

from . import views


app_name = 'bridges'

urlpatterns = [
    re_path(
        r'^transactions/(?P<scope>(profile|sheet|record))$',
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
