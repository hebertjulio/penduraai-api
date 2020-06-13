from django.urls import path

from . import views


app_name = 'notebooks'

urlpatterns = [
    path(
        'records',
        views.RecordListView.as_view(),
        name='record_list'),
    path(
        'records/<int:pk>',
        views.RecordDetailView.as_view(),
        name='record_detail'),
    path(
        'records/<int:pk>/strikethrough',
        views.RecordStrikethroughView.as_view(),
        name='record_strikethrough'),
    path(
        'customer-records',
        views.CustomerRecordListView.as_view(),
        name='customer_record_list'),
    path(
        'customer-records/<int:pk>',
        views.CustomerRecordDetailView.as_view(),
        name='customer_record_detail'),
    path(
        'customer-records/creditor/<int:pk>',
        views.DebtorCustomerRecordView.as_view(),
        name='debtor_customer_record'),
    path(
        'creditors',
        views.CreditorListView.as_view(),
        name='creditor_list'),
    path(
        'debtors',
        views.DebtorListView.as_view(),
        name='debtor_list'),
    path(
        'transactions/new-record',
        views.TransactionNewRecordView.as_view(),
        name='transaction_new_record'),
    path(
        'transactions/new-customer-record',
        views.TransactionNewCustomerRecordView.as_view(),
        name='transaction_new_customer_record'),
    path(
        'transactions/<str:pk>',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'),
    path(
        'transactions/<str:pk>/reject',
        views.TransactionRejectView.as_view(),
        name='transaction_reject'),
]
