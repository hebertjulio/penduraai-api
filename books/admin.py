from django.contrib import admin

from .models import Record, Customer


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'creditor', 'seller', 'debtor', 'buyer',
        'value', 'operation', 'status',
    )
    search_fields = (
        'creditor__name', 'creditor__email',
        'debtor__name', 'debtor__email',
        'uuid',
    )
    autocomplete_fields = (
        'creditor', 'debtor', 'seller',
        'buyer',
    )
    list_filter = (
        'operation', 'status',
    )
    ordering = (
        '-created',
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'creditor', 'debtor', 'authorized',
    )
    search_fields = (
        'creditor__name', 'creditor__email',
        'debtor__name', 'debtor__email',
    )
    autocomplete_fields = (
        'creditor', 'debtor',
    )
    list_filter = (
        'authorized',
    )
    ordering = (
        'creditor__id', 'debtor__name',
    )
