from django.urls import path

from . import views


app_name = 'cashbooks'

urlpatterns = [
    path(
        'transactions',
        views.TransactionListView.as_view(),
        name='transaction_list'),
    path(
        'creditors',
        views.CreditorListView.as_view(),
        name='creditor_list'),
    path(
        'debtors',
        views.DebtorListView.as_view(),
        name='debtor_list'),
]
