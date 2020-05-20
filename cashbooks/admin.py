from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'creditor', 'debtor', 'description', 'type',
        'value', 'status',
    )
    search_fields = (
        'creditor__name', 'creditor__email', 'debtor__name',
        'debtor__email', 'description',
    )
    list_filter = (
        'status',
    )
    ordering = (
        'created',
    )
