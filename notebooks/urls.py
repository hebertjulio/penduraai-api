from django.urls import path

from . import views


app_name = 'notebooks'

urlpatterns = [
    path(
        'records/ticket/<str:ticket_id>',
        views.RecordConfirmView.as_view(),
        name='record_confirm'),
    path(
        'records',
        views.RecordListView.as_view(),
        name='record_list'),
    path(
        'records/<int:record_id>',
        views.RecordDetailView.as_view(),
        name='record_detail'),
    path(
        'sheets/ticket/<str:ticket_id>',
        views.SheetConfirmView.as_view(),
        name='sheet_confirm'),
    path(
        'sheets',
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
