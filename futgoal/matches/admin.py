from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Match, MatchNote, MatchPlayerStats


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
        'away_team__name',
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


@admin.register(MatchNote)
class MatchNoteAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'match',
        'rival_team',
        'short_content',
        'created'
    ]

    list_filter = [
        'match__status',
        'match__match_type',
        'match__season',
        'created'
    ]

    search_fields = [
        'title',
        'content',
        'match__away_team__name',
        'match__home_team__name'
    ]

    readonly_fields = ['created', 'modified', 'rival_team']

    fieldsets = (
        (_('Información de la Nota'), {
            'fields': (
                'match',
                'title',
                'content'
            )
        }),
        (_('Información del Partido'), {
            'fields': ('rival_team',),
            'classes': ('collapse',)
        }),
        (_('Auditoría'), {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )

    date_hierarchy = 'created'

    def short_content(self, obj):
        return obj.short_content
    short_content.short_description = _('Contenido Resumido')

    def rival_team(self, obj):
        return obj.rival_team
    rival_team.short_description = _('Equipo Rival')


@admin.register(MatchPlayerStats)
class MatchPlayerStatsAdmin(admin.ModelAdmin):
    list_display = [
        'match',
        'player',
        'status',
        'minutes_played',
        'goals',
        'assists',
        'yellow_cards',
        'red_cards',
        'rating'
    ]

    list_filter = [
        'status',
        'match__season',
        'match__match_date',
        'goals',
        'assists',
        'yellow_cards',
        'red_cards'
    ]

    search_fields = [
        'player__first_name',
        'player__last_name',
        'player__sport_name',
        'match__away_team__name'
    ]

    readonly_fields = ['created', 'modified']

    fieldsets = (
        (_('Información Básica'), {
            'fields': (
                'match',
                'player',
                'status'
            )
        }),
        (_('Estadísticas de Juego'), {
            'fields': (
                'minutes_played',
                'goals',
                'assists',
                'yellow_cards',
                'red_cards'
            )
        }),
        (_('Sustituciones'), {
            'fields': (
                'substitution_in',
                'substitution_out'
            ),
            'classes': ('collapse',)
        }),
        (_('Evaluación'), {
            'fields': (
                'rating',
                'performance_notes'
            ),
            'classes': ('collapse',)
        }),
        (_('Auditoría'), {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )

    date_hierarchy = 'match__match_date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('match', 'player', 'match__season')
