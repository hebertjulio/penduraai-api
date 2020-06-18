from django.urls import path

from . import views


app_name = 'bridges'

urlpatterns = [
    path(
        'transactions/record',
        views.TransactionRecordView.as_view(),
        name='transaction_record'),
    path(
        'transactions/sheet',
        views.TransactionSheetView.as_view(),
        name='transaction_sheet'),
    path(
        'transactions/profile',
        views.TransactionProfileView.as_view(),
        name='transaction_profile'),
    path(
        'transactions/<str:key>',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'),
]
