from django.urls import path

from . import views


app_name = 'notebooks'

urlpatterns = [
    path(
        'records/request',
        views.RecordRequestView.as_view(),
        name='record_request'),
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
        'sheets/<int:pk>/buyer/<int:profile_id>',
        views.SheetBuyerManageView.as_view(),
        name='sheet_buyer_manage'),
    path(
        'balances-by-merchant',
        views.BalanceListByMerchantView.as_view(),
        name='balance_list_by_merchant'),
    path(
        'balances-by-customer',
        views.BalanceListByCustomerView.as_view(),
        name='balance_list_by_customer'),
]
