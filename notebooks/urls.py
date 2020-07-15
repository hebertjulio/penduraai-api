from django.urls import path

from . import views


app_name = 'notebooks'

urlpatterns = [
    path(
        'records/request',
        views.RecordRequestView.as_view(),
        name='record_request'),
    path(
        'records/transaction/<int:pk>',
        views.RecordCreateView.as_view(),
        name='record_create'),
    path(
        'records',
        views.RecordListView.as_view(),
        name='record_list'),
    path(
        'records/<int:pk>',
        views.RecordDetailView.as_view(),
        name='record_detail'),
    path(
        'sheets/request',
        views.SheetRequestView.as_view(),
        name='sheet_request'),
    path(
        'sheets',
        views.SheetListView.as_view(),
        name='sheet_list'),
    path(
        'sheets/<int:pk>',
        views.SheetDetailView.as_view(),
        name='sheet_detail'),
    path(
        'sheets/<int:pk>/profile/<int:profile_id>',
        views.SheetProfileManageView.as_view(),
        name='sheet_profile_manage'),
    path(
        'balances-by-merchant',
        views.BalanceListByMerchantView.as_view(),
        name='balance_list_by_merchant'),
    path(
        'balances-by-customer',
        views.BalanceListByCustomerView.as_view(),
        name='balance_list_by_customer'),
]
