from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditModel(models.Model):
    """
    Modelo base abstracto que proporciona campos de auditoría automáticos.
    """
    created = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True
    )
    modified = models.DateTimeField(
        _('Fecha de modificación'),
        auto_now=True
    )
    created_by = models.ForeignKey(
        'users.User',
        verbose_name=_('Creado por'),
        related_name='%(class)s_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    modified_by = models.ForeignKey(
        'users.User',
        verbose_name=_('Modificado por'),
        related_name='%(class)s_modified',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
