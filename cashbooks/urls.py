from django.urls import path

from . import views


app_name = 'cashbooks'

urlpatterns = [
    path(
        'records',
        views.RecordListView.as_view(),
        name='record_list'),
    path(
        'creditors',
        views.CreditorListView.as_view(),
        name='creditor_list'),
    path(
        'debtors',
        views.DebtorListView.as_view(),
        name='debtor_list'),
    path(
        'allowed-debtors',
        views.AllowedDebtorListView.as_view(),
        name='allowed_debtor_list'),
    path(
        'allowed-debtors/<int:pk>',
        views.AllowedDebtorDetailView.as_view(),
        name='allowed_debtor_detail'),
    path(
        'transactions',
        views.TransactionListView.as_view(),
        name='transaction_list'),
]
