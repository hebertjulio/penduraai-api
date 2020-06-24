from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'scope', 'data', 'expire_at', 'status',
    )
    search_fields = (
        'data', 'scope',
    )
    list_filter = (
        'status', 'created',
    )
    ordering = (
        '-created',
    )
