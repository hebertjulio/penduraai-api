from django.contrib import admin

from .models import Record, Whitelist


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'creditor', 'debtor', 'operation', 'value',
        'seller', 'buyer',
    )
    search_fields = (
        'creditor__name', 'creditor__email',
        'debtor__name', 'debtor__email',
        'id',
    )
    autocomplete_fields = (
        'creditor', 'debtor', 'seller',
        'buyer',
    )
    list_filter = (
        'operation',
    )
    ordering = (
        'created',
    )


@admin.register(Whitelist)
class WhitelistAdmin(admin.ModelAdmin):
    list_display = (
        'creditor', 'debtor', 'status',
    )
    search_fields = (
        'creditor__name', 'creditor__email',
        'debtor__name', 'debtor__email',
    )
    autocomplete_fields = (
        'creditor', 'debtor',
    )
    list_filter = (
        'status',
    )
    ordering = (
        'creditor__id', 'debtor__name',
    )
