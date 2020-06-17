from django.urls import path

from . import views


app_name = 'notebooks'

urlpatterns = [
    path(
        'records/create/<str:token>',
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
        'sheets/create/<str:token>',
        views.SheetCreateView.as_view(),
        name='sheet_create'),
    path(
        'sheets/<int:pk>',
        views.SheetDetailView.as_view(),
        name='sheet_detail'),
    path(
        'buyers',
        views.BuyerListView.as_view(),
        name='buyer_list'),
    path(
        'buyers/<int:pk>',
        views.BuyerDetailView.as_view(),
        name='buyer_detail'),
    path(
        'balances-by-store',
        views.BalanceListByStoreView.as_view(),
        name='balance_list_by_store'),
    path(
        'balances-by-customer',
        views.BalanceListByCustomerView.as_view(),
        name='balance_list_by_customer'),
]
