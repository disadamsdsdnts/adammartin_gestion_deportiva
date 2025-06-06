from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MatchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'futgoal.matches'
    verbose_name = _('Partidos')
