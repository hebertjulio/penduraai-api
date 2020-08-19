from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'scope', 'payload', 'expire_at', 'usage',
        'ws_notification', 'push_notification'
    )
    search_fields = (
        'user__name', 'user__email',
    )
    list_filter = (
        'scope', 'created',
    )
    ordering = (
        '-created',
    )
