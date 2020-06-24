from django.urls import path

from . import views


app_name = 'bridges'

urlpatterns = [
    path(
        'transactions/<int:pk>',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'),
    path(
        'transactions/<int:pk>/reject',
        views.TransactionRejectView.as_view(),
        name='transaction_reject'),
]
