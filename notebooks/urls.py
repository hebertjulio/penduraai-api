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
        'sheets',
        views.SheetListView.as_view(),
        name='sheet_list'),
    path(
        'sheets/<int:pk>',
        views.SheetDetailView.as_view(),
        name='sheet_detail'),
    path(
        'sheets/store/<int:pk>',
        views.SheetDetailByStoreView.as_view(),
        name='sheet_detail_by_store'),
    path(
        'balances-by-store',
        views.BalanceListByStoreView.as_view(),
        name='balance_list_by_store'),
    path(
        'balances-by-customer',
        views.BalanceListByCustomerView.as_view(),
        name='balance_list_by_customer'),
    path(
        'transactions/new-record',
        views.TransactionNewRecordView.as_view(),
        name='transaction_new_record'),
    path(
        'transactions/new-sheet',
        views.TransactionNewSheetView.as_view(),
        name='transaction_new_sheet'),
    path(
        'transactions/<str:pk>',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'),
    path(
        'transactions/<str:pk>/reject',
        views.TransactionRejectView.as_view(),
        name='transaction_reject'),
]
