from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator

from futgoal.utils.models import AuditModel


class Player(AuditModel):
    first_name = models.CharField(
        _('Nombre'),
        max_length=100,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        _('Apellido'),
        max_length=100,
        blank=True,
        null=True
    )
    birth_date = models.DateField(
        _('Fecha de nacimiento'),
        blank=True,
        null=True
    )
    identity_document = models.CharField(
        _('Documento de identidad'),
        max_length=100,
        blank=True,
        null=True
    )
    sport_name = models.CharField(
        _('Nombre deportivo'),
        max_length=100,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('Email'),
        validators=[EmailValidator()],
        unique=False,
        null=True,
        blank=True
    )
    phone = models.CharField(
        _('Teléfono'),
        max_length=100,
        blank=True,
        null=True
    )
    position = models.CharField(
        _('Posición'),
        max_length=100,
        blank=True,
        null=True
    )
    dorsal = models.PositiveIntegerField(
        _('Dorsal'),
        blank=True,
        null=True,
        help_text=_('Número de dorsal del jugador')
    )
    country = models.CharField(
        _('País'),
        max_length=100,
        blank=True,
        null=True
    )
    address = models.CharField(
        _('Dirección'),
        max_length=100,
        blank=True,
        null=True
    )
    city = models.CharField(
        _('Ciudad'),
        max_length=100,
        blank=True,
        null=True
    )
    municipality = models.CharField(
        _('Municipio'),
        max_length=100,
        blank=True,
        null=True
    )
    postal_code = models.CharField(
        _('Código postal'),
        max_length=100,
        blank=True,
        null=True
    )
    region = models.CharField(
        _('Comunidad Autónoma'),
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

    def __str__(self) -> str:
        return str(self.first_name + ' ' + self.last_name)

    @property
    def full_name(self):
        """
        Retorna el nombre completo del jugador
        """
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    class Meta:
        verbose_name = _('Jugador')
        verbose_name_plural = _('Jugadores')
        ordering = ['-created']
