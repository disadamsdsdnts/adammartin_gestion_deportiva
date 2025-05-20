from django.db import models
from django.utils.translation import gettext_lazy as _
from futgoal.utils.models import SingletonModel

class Team(SingletonModel):
    name = models.CharField(
        _('Nombre del equipo'),
        max_length=140
    )
    logo = models.ImageField(
        _('Escudo'),
        upload_to='teams/logos/',
        blank=True,
        null=True
    )
    city = models.CharField(
        _('Ciudad'),
        max_length=100,
        blank=True,
        null=True
    )
    country = models.CharField(
        _('País'),
        max_length=100,
        blank=True,
        null=True
    )
    foundation_date = models.DateField(
        _('Fecha de fundación'),
        blank=True,
        null=True
    )
    coach = models.CharField(
        _('Entrenador'),
        max_length=140,
        blank=True,
        null=True
    )
    description = models.TextField(
        _('Descripción'),
        blank=True,
        null=True
    )
    website = models.URLField(
        _('Página web oficial'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Equipo')
        verbose_name_plural = _('Equipo')

    def __str__(self):
        return self.name
