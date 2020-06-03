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
    re_path(
        r'^customers/(?P<by>(debtor|creditor))$',
        views.CustomerBalanceListView.as_view(),
        name='customer_balance_list'),
    path(
        'customers',
        views.CustomerListView.as_view(),
        name='customer_list'),
    path(
        'customers/<int:pk>',
        views.CustomerDetailView.as_view(),
        name='customer_detail'),
]
