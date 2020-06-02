from django.urls import path

from . import views


app_name = 'brokers'

urlpatterns = [
    path(
        'transactions',
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
