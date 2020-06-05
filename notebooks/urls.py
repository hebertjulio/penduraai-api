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
        r'records/(?P<pk>\w+)/(?P<switch>(strikethrough|clean))',
        views.RecordStrikethroughView.as_view(),
        name='record_strikethrough'),
    path(
        'customers',
        views.CustomerListView.as_view(),
        name='customer_list'),
    path(
        'customers/<int:pk>',
        views.CustomerDetailView.as_view(),
        name='customer_detail'),
    path(
        'creditors',
        views.CreditorListView.as_view(),
        name='creditor_list'),
    path(
        'debtors',
        views.DebtorListView.as_view(),
        name='debtor_list'),
]
