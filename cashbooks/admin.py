from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'creditor', 'debtor', 'operation', 'value',
        'requester', 'subscriber',
    )
    search_fields = (
        'creditor__name', 'creditor__email', 'debtor__name',
        'debtor__email', 'description',
    )
    autocomplete_fields = (
        'creditor', 'debtor', 'requester', 'subscriber',
    )
    list_filter = (
        'operation',
    )
    ordering = (
        'created',
    )
