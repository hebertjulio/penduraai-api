from django.contrib import admin

from .models import Record, Sheet, Buyer


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sheet', 'attendant', 'signature',
        'value', 'operation', 'is_active',
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
        'operation', 'is_active',
    )
    ordering = (
        '-created',
    )


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'store', 'customer', 'is_active',
    )
    search_fields = (
        'store__name', 'store__email',
        'customer__name', 'customer__email',
    )
    autocomplete_fields = (
        'store', 'customer',
    )
    list_filter = (
        'is_active',
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
        'sheet__customer__name', 'sheet__customer__email',
        'sheet__store__name', 'sheet__store__email',
        'sheet__id',
    )
    autocomplete_fields = (
        'sheet', 'profile',
    )
    ordering = (
        'sheet__id',
    )
