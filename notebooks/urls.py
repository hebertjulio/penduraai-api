from django.urls import path, re_path

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
    re_path(
        '(?P<switch>(debtors|creditors))',
        views.DebtorCreditorListView.as_view(),
        name='debtor_creditor_list'),
    re_path(
        'transactions/(?P<switch>(new-record|new-customer-record))',
        views.TransactionListView.as_view(),
        name='transaction_list'),
    path(
        'transactions/<str:pk>',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'),
    path(
        'transactions/<str:pk>/reject',
        views.TransactionRejectView.as_view(),
        name='transaction_reject'),
]
