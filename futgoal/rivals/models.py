from django.db import models
from django.utils.translation import gettext_lazy as _
from futgoal.utils.models import AuditModel


class Rival(AuditModel):
    """
    Modelo para gestionar equipos rivales.
    """
    name = models.CharField(
        _('Nombre del rival'),
        max_length=140,
        help_text=_('Nombre del equipo rival')
    )
    coach_name = models.CharField(
        _('Nombre del entrenador'),
        max_length=140,
        blank=True,
        null=True,
        help_text=_('Nombre del entrenador del equipo rival')
    )
    field_name = models.CharField(
        _('Nombre del campo'),
        max_length=140,
        blank=True,
        null=True,
        help_text=_('Nombre del campo de juego del equipo rival')
    )
    city = models.CharField(
        _('Ciudad'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Ciudad donde se encuentra el equipo rival')
    )
    coach_phone = models.CharField(
        _('Teléfono del entrenador'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('Número de teléfono del entrenador')
    )
    coach_email = models.EmailField(
        _('Email del entrenador'),
        blank=True,
        null=True,
        help_text=_('Correo electrónico del entrenador')
    )
    notes = models.TextField(
        _('Notas del equipo'),
        blank=True,
        null=True,
        help_text=_('Notas adicionales sobre el equipo rival')
    )

    class Meta:
        verbose_name = _('Rival')
        verbose_name_plural = _('Rivales')
        ordering = ['name']

    def __str__(self):
        return str(self.name)
