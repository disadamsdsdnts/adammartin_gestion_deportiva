from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User, ActionLogUser


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""

    list_display = [
        'email',
        'full_name',
        'first_name',
        'last_name',
        'position',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login'
    ]

    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login',
        'sale_team'
    ]

    search_fields = [
        'email',
        'first_name',
        'last_name',
        'full_name',
        'position'
    ]

    ordering = ['email']

    readonly_fields = [
        'uuid',
        'remember_key',
        'magic_link_field',
        'date_joined',
        'last_login'
    ]

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Información Personal'), {
            'fields': (
                'first_name',
                'last_name',
                'full_name',
                'position',
                'base_salary'
            )
        }),
        (_('Permisos'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Fechas Importantes'), {
            'fields': ('last_login', 'date_joined')
        }),
        (_('Configuración Avanzada'), {
            'fields': (
                'sale_team',
                'uuid',
                'remember_key',
                'magic_link_field',
                'pre_email'
            ),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'position',
                'is_active',
                'is_staff'
            ),
        }),
    )

    def magic_link_field(self, obj):
        """Display magic login link as clickable link."""
        if obj.uuid:
            return mark_safe(f'<a href="{obj.magic_login_link}" target="_blank">{obj.magic_login_link}</a>')
        return "-"
    magic_link_field.short_description = _("Enlace de acceso directo")

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('sale_team')


@admin.register(ActionLogUser)
class ActionLogUserAdmin(admin.ModelAdmin):
    """Admin configuration for ActionLogUser model."""

    list_display = [
        'created',
        'user_link',
        'action_description',
        'modified'
    ]

    list_filter = [
        'created',
        'modified',
        'user__is_active'
    ]

    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'action_description'
    ]

    readonly_fields = [
        'created',
        'modified',
        'user',
        'action_description'
    ]

    ordering = ['-created']

    date_hierarchy = 'created'

    def user_link(self, obj):
        """Display user as clickable link to user admin."""
        url = reverse('admin:users_user_change', args=[obj.user.pk])
        return mark_safe(f'<a href="{url}">{obj.user.full_name or obj.user.email}</a>')
    user_link.short_description = _("Usuario")
    user_link.admin_order_field = 'user__email'

    def has_add_permission(self, request):
        """Disable manual creation of action logs."""
        return False

    def has_change_permission(self, request, obj=None):
        """Make action logs read-only."""
        return False

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


# Customize admin site headers
admin.site.site_header = _("Administración de FutGoal")
admin.site.site_title = _("FutGoal Admin")
admin.site.index_title = _("Panel de Administración")
