from django.contrib import admin
from .models import Rival


@admin.register(Rival)
class RivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach_name', 'city', 'field_name', 'get_seasons', 'created', 'modified')
    list_filter = ('city', 'seasons', 'created', 'modified')
    search_fields = ('name', 'coach_name', 'city', 'field_name')
    ordering = ('name',)
    filter_horizontal = ('seasons',)

    def get_seasons(self, obj):
        """Retorna las temporadas del rival separadas por comas."""
        return ", ".join([season.name for season in obj.seasons.all()])
    get_seasons.short_description = 'Temporadas'

    fieldsets = (
        ('Información del Equipo', {
            'fields': ('name', 'city', 'field_name')
        }),
        ('Información del Entrenador', {
            'fields': ('coach_name', 'coach_phone', 'coach_email')
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
