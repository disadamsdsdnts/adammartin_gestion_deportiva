from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Season(models.Model):
    name = models.CharField(_('Nombre'), max_length=100)
    start_date = models.DateField(_('Fecha de inicio'))
    end_date = models.DateField(_('Fecha de fin'))
    is_active = models.BooleanField(_('Activa'), default=False)
    created_at = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Última actualización'), auto_now=True)

    class Meta:
        verbose_name = _('Temporada')
        verbose_name_plural = _('Temporadas')
        ordering = ['-start_date']

    def __str__(self):
        return str(self.name)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_('La fecha de inicio debe ser anterior a la fecha de fin'))

    def save(self, *args, **kwargs):
        if self.is_active:
            # Desactivar todas las otras temporadas
            Season.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_active(cls):
        """
        Obtiene la temporada activa actual.
        Returns:
            Season: La temporada activa o None si no hay ninguna.
        """
        try:
            return cls.objects.get(is_active=True)
        except cls.DoesNotExist:
            return None
