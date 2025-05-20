from django.db import models
from django.utils.translation import gettext_lazy as _

class Season(models.Model):
    name = models.CharField(_('Nombre'), max_length=100)
    start_date = models.DateField(_('Fecha de inicio'))
    end_date = models.DateField(_('Fecha de fin'))
    is_active = models.BooleanField(_('Activa'), default=True)
    created_at = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Fecha de actualización'), auto_now=True)

    class Meta:
        verbose_name = _('Temporada')
        verbose_name_plural = _('Temporadas')
        ordering = ['-start_date']

    def __str__(self):
        return self.name
