from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'data', 'expire_at', 'tickets'
    )
    search_fields = (
        'user__name', 'user__email',
    )
    list_filter = (
        'created',
    )
    ordering = (
        '-created',
    )
