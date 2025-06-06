from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from futgoal.utils.models import AuditModel
from .match import Match


class MatchNote(AuditModel):
    """
    Modelo que representa una nota individual de un partido.
    Permite tener múltiples notas por partido con fecha y la posibilidad de eliminarlas.
    """

    match = models.ForeignKey(
        Match,
        verbose_name=_('Partido'),
        on_delete=models.CASCADE,
        related_name='match_notes'
    )

    title = models.CharField(
        _('Título'),
        max_length=200,
        help_text=_('Título breve de la nota')
    )

    content = models.TextField(
        _('Contenido'),
        help_text=_('Contenido detallado de la nota')
    )

    class Meta:
        verbose_name = _('Nota de Partido')
        verbose_name_plural = _('Notas de Partido')
        ordering = ['-created']

    def __str__(self):
        return f"{self.title} - {self.match}"

    def get_absolute_url(self):
        return reverse('matches:match_note_detail', kwargs={'pk': self.pk})

    @property
    def rival_team(self):
        """Retorna el nombre del equipo rival"""
        return self.match.away_team.name

    @property
    def short_content(self):
        """Retorna una versión corta del contenido para listados"""
        if self.content and len(self.content) > 100:
            return f"{self.content[:100]}..."
        return self.content or ""
