from django.contrib import admin

from .models import Record, Sheet


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'store', 'customer', 'attendant', 'accept',
        'value', 'operation', 'is_deleted',
    )
    search_fields = (
        'sheetrecord__store__name', 'sheetrecord__store__email',
        'sheetrecord__customer__name', 'sheetrecord__customer__email',
        'id',
    )
    autocomplete_fields = (
        'sheet', 'attendant', 'accept',
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
        'store', 'customer', 'authorized',
    )
    search_fields = (
        'store__name', 'store__email',
        'customer__name', 'customer__email',
    )
    autocomplete_fields = (
        'store', 'customer',
    )
    list_filter = (
        'authorized',
    )
    ordering = (
        'store__id', 'customer__name',
    )
