from django.contrib import admin

from .models import Record, Sheet, Buyer


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sheet', 'attendant', 'signature',
        'value', 'operation', 'is_deleted',
    )
    search_fields = (
        'sheet__store__name', 'sheet__store__email',
        'sheet__customer__name', 'sheet__customer__email',
        'id',
    )
    autocomplete_fields = (
        'sheet', 'attendant', 'signature',
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


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = (
        'sheet', 'profile',
    )
    search_fields = (
        'sheet__store__name', 'sheet__store__email',
    )
    autocomplete_fields = (
        'sheet', 'profile',
    )
