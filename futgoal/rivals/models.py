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
    seasons = models.ManyToManyField(
        'season.Season',
        verbose_name=_('Temporadas'),
        help_text=_('Temporadas en las que participa este equipo rival'),
        blank=True
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

    @classmethod
    def get_by_active_season(cls):
        """
        Obtiene todos los rivales de la temporada activa.
        """
        from futgoal.season.models import Season
        active_season = Season.get_active()
        if active_season:
            return cls.objects.filter(seasons=active_season)
        return cls.objects.none()

    @classmethod
    def get_by_season(cls, season):
        """
        Obtiene todos los rivales de una temporada específica.
        """
        return cls.objects.filter(seasons=season)

    def is_in_active_season(self):
        """
        Verifica si este rival está en la temporada activa.
        """
        from futgoal.season.models import Season
        active_season = Season.get_active()
        if active_season:
            return self.seasons.filter(id=active_season.id).exists()
        return False
