from django.urls import path

from . import views


app_name = 'cashbooks'

urlpatterns = [
    path(
        'transactions',
        views.TransactionListView.as_view(),
        name='transaction_list'),
]
