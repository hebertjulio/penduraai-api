from django.contrib import admin

from .models import Record, CustomerRecord


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'creditor', 'seller', 'debtor', 'buyer',
        'value', 'operation',
    )
    search_fields = (
        'customerrecord__creditor__name', 'customerrecord__creditor__email',
        'customerrecord__debtor__name', 'customerrecord__debtor__email',
        'id',
    )
    autocomplete_fields = (
        'customer_record', 'seller', 'buyer',
    )
    list_filter = (
        'operation',
    )
    ordering = (
        '-created',
    )


@admin.register(CustomerRecord)
class CustomerRecordAdmin(admin.ModelAdmin):
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
