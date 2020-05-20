from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': (
            'name', 'email', 'password',)}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'user_permissions',),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'created', 'modified',)}),
    )
    list_display = (
        'name', 'email', 'is_active', 'is_staff', 'is_superuser',
    )
    search_fields = (
        'name', 'email',
    )
    readonly_fields = (
        'last_login', 'created', 'modified',
    )
    add_fieldsets = (
        (None, {
            'fields': ('name', 'email',),
        }),
    ) + BaseUserAdmin.add_fieldsets
    ordering = (
        'name',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'accountable', 'name', 'role', 'pin',
    )
    search_fields = (
        'accountable__name', 'accountable__email', 'name',
    )
    readonly_fields = (
        'created', 'modified', 'accountable',
    )
    list_filter = (
        'role',
    )
    ordering = (
        'accountable__name',
    )
