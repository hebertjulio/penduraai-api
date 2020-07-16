from django.urls import path, re_path

from . import views


app_name = 'notebooks'

urlpatterns = [
    path(
        'records/request',
        views.RecordRequestView.as_view(),
        name='record_request'),
    path(
        'records/transaction/<int:transaction_id>',
        views.RecordCreateView.as_view(),
        name='record_create'),
    path(
        'records',
        views.RecordListView.as_view(),
        name='record_list'),
    path(
        'records/<int:record_id>',
        views.RecordDetailView.as_view(),
        name='record_detail'),
    path(
        'sheets/request',
        views.SheetRequestView.as_view(),
        name='sheet_request'),
    path(
        'sheets/transaction/<int:transaction_id>',
        views.SheetCreateView.as_view(),
        name='sheet_create'),
    re_path(
        r'sheets/(?P<by>(merchant|customer))',
        views.SheetListView.as_view(),
        name='sheet_list'),
    path(
        'sheets/<int:sheet_id>',
        views.SheetDetailView.as_view(),
        name='sheet_detail'),
    path(
        'sheets/<int:sheet_id>/buyer/<int:profile_id>',
        views.SheetBuyerView.as_view(),
        name='sheet_buyer'),
]
