from django.contrib import admin

from .models import Record, AllowedDebtor


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


@admin.register(AllowedDebtor)
class AllowedDebtorAdmin(admin.ModelAdmin):
    list_display = (
        'creditor', 'debtor', 'is_active',
    )
    search_fields = (
        'creditor__name', 'creditor__email',
        'debtor__name', 'debtor__email',
    )
    autocomplete_fields = (
        'creditor', 'debtor',
    )
    list_filter = (
        'is_active',
    )
    ordering = (
        'creditor__id', 'debtor__name',
    )
