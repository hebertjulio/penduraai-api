from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'profile', 'scope', 'data', 'expire_at',
        'status',
    )
    search_fields = (
        'user__name', 'user__email',
    )
    list_filter = (
        'status', 'created',
    )
    ordering = (
        '-created',
    )
