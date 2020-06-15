from django.contrib import admin

from .models import Record, Sheet


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sheet', 'attendant', 'subscriber',
        'value', 'operation', 'is_deleted',
    )
    search_fields = (
        'sheetrecord__store__name', 'sheetrecord__store__email',
        'sheetrecord__customer__name', 'sheetrecord__customer__email',
        'id',
    )
    autocomplete_fields = (
        'sheet', 'attendant', 'subscriber',
    )
    list_filter = (
        'operation', 'is_deleted',
    )
    ordering = (
        '-created',
    )


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = (
        'store', 'customer', 'is_authorized',
    )
    search_fields = (
        'store__name', 'store__email',
        'customer__name', 'customer__email',
    )
    autocomplete_fields = (
        'store', 'customer',
    )
    list_filter = (
        'is_authorized',
    )
    ordering = (
        'store__id', 'customer__name',
    )
