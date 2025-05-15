from django.db import models
from django.utils.translation import gettext_lazy as _
from futgoal.models import AuditModel

class Player(AuditModel):
    """Modelo para gestionar los jugadores."""
    first_name = models.CharField(_('Nombre'), max_length=100)
    last_name = models.CharField(_('Apellidos'), max_length=100)
    identity_document = models.CharField(_('Documento de identidad'), max_length=20, unique=True)
    sport_name = models.CharField(_('Nombre deportivo'), max_length=100, blank=True, null=True)
    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_('Teléfono'), max_length=20)
    photo = models.ImageField(_('Foto'), upload_to='players/photos/', null=True, blank=True)
    position = models.CharField(_('Posición'), max_length=50)
    country = models.CharField(_('País'), max_length=100)
    biography = models.TextField(_('Biografía'), blank=True, null=True)
    is_active = models.BooleanField(_('Activo'), default=True)

    # Campos de dirección
    address = models.CharField(_('Dirección'), max_length=255)
    city = models.CharField(_('Ciudad'), max_length=100)
    municipality = models.CharField(_('Municipio'), max_length=100)
    postal_code = models.CharField(_('Código postal'), max_length=10)

    class Meta:
        verbose_name = _('Jugador')
        verbose_name_plural = _('Jugadores')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def display_name(self):
        return self.sport_name or self.full_name
