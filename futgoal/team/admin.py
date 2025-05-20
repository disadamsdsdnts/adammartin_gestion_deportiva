from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Solo permitir añadir si no existe ya un objeto Team
        return not Team.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # No permitir borrar el singleton
        return False
