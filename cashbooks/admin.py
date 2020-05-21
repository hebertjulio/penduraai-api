from django.contrib import admin

from .models import Transaction, Whitelist


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'creditor', 'debtor', 'operation', 'value',
        'requester', 'signatory',
    )
    search_fields = (
        'creditor__name', 'creditor__email',
        'debtor__name', 'debtor__email',
        'description',
    )
    autocomplete_fields = (
        'creditor', 'debtor', 'requester',
        'signatory',
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
        'owner', 'customer', 'status',
    )
    search_fields = (
        'owner__name', 'owner__email',
        'customer__name','customer__email',
    )
    autocomplete_fields = (
        'owner', 'customer',
    )
    list_filter = (
        'status',
    )
    ordering = (
        'owner__id', 'customer__name',
    )
