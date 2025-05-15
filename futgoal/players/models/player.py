from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator

from futgoal.utils.models import AuditModel


class Player(AuditModel):
    name = models.CharField(
        _('Nombre'),
        max_length=255,
        default=''
    )
    email = models.EmailField(
        _('Email'),
        validators=[EmailValidator()],
        unique=False,
        null=True,
        blank=True
    )
    biography = models.TextField(
        _('Biografía'),
        blank=True,
        null=True
    )
    position = models.CharField(
        _('Posición'),
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
    photo = models.ImageField(
        _('Foto'),
        upload_to='players/photos/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _('Activo'),
        default=True
    )

    class Meta:
        verbose_name = _('Jugador')
        verbose_name_plural = _('Jugadores')
        ordering = ['-created']

    def __str__(self) -> str:
        return str(self.name)
