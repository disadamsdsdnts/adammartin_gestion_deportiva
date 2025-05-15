from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from futgoal.players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = _('Nombre completo')
    get_full_name.admin_order_field = 'first_name'

    def get_sport_name(self, obj):
        return obj.sport_name
    get_sport_name.short_description = _('Nombre deportivo')
    get_sport_name.admin_order_field = 'sport_name'

    def get_identity_document(self, obj):
        return obj.identity_document
    get_identity_document.short_description = _('Documento de identidad')
    get_identity_document.admin_order_field = 'identity_document'

    def get_phone(self, obj):
        return obj.phone
    get_phone.short_description = _('Teléfono')
    get_phone.admin_order_field = 'phone'

    list_display = ('get_full_name', 'get_sport_name', 'get_identity_document', 'email', 'get_phone', 'position', 'country', 'is_active')
    list_filter = ('is_active', 'position', 'country')
    search_fields = ('first_name', 'last_name', 'sport_name', 'identity_document', 'email', 'phone', 'biography')
    fieldsets = (
        (_('Información personal'), {
            'fields': (
                'first_name', 'last_name', 'identity_document', 'sport_name',
                'email', 'phone', 'photo'
            )
        }),
        (_('Dirección'), {
            'fields': (
                'address', 'city', 'municipality', 'postal_code'
            )
        }),
        (_('Información deportiva'), {
            'fields': (
                'position', 'country', 'biography'
            )
        }),
        (_('Estado'), {
            'fields': (
                'is_active',
            )
        }),
    )
