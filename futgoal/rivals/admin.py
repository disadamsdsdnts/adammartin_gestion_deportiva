from django.contrib import admin
from .models import Rival


@admin.register(Rival)
class RivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach_name', 'city', 'field_name', 'created', 'modified')
    list_filter = ('city', 'created', 'modified')
    search_fields = ('name', 'coach_name', 'city', 'field_name')
    ordering = ('name',)

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
