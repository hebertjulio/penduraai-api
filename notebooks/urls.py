from django.urls import path

from . import views


app_name = 'books'

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
        'customers',
        views.CustomerListView.as_view(),
        name='customer_list'),
    path(
        'customers/<int:pk>',
        views.CustomerDetailView.as_view(),
        name='customer_detail'),
]
