from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        'match_date',
        'home_team',
        'away_team',
        'match_type',
        'status',
        'result',
        'is_home',
        'season'
    ]

    list_filter = [
        'status',
        'match_type',
        'is_home',
        'season',
        'match_date'
    ]

    search_fields = [
        'away_team',
        'venue',
        'notes'
    ]

    readonly_fields = ['created', 'modified']

    fieldsets = (
        (_('Información del Partido'), {
            'fields': (
                'season',
                'away_team',
                'match_date',
                'venue',
                'is_home'
            )
        }),
        (_('Detalles del Partido'), {
            'fields': (
                'match_type',
                'status',
                'home_score',
                'away_score',
                'notes'
            )
        }),
        (_('Auditoría'), {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )

    date_hierarchy = 'match_date'

    def result(self, obj):
        return obj.result
    result.short_description = _('Resultado')
