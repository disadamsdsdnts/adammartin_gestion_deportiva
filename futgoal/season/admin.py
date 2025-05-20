from django.contrib import admin
from .models import Season

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name',)
    ordering = ('-start_date',)
