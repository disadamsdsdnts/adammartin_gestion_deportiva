from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

from futgoal.utils.models import AuditModel
from futgoal.season.models import Season
from futgoal.team.models import Team
from futgoal.rivals.models import Rival


class Match(AuditModel):
    """
    Modelo que representa un partido.
    Los partidos se asocian automáticamente con la temporada activa.
    """

    MATCH_STATUS_CHOICES = [
        ('scheduled', _('Programado')),
        ('in_progress', _('En curso')),
        ('finished', _('Finalizado')),
        ('cancelled', _('Cancelado')),
        ('postponed', _('Aplazado')),
    ]

    MATCH_TYPE_CHOICES = [
        ('friendly', _('Amistoso')),
        ('league', _('Liga')),
        ('cup', _('Copa')),
        ('playoff', _('Playoff')),
        ('training', _('Entrenamiento')),
    ]

    season = models.ForeignKey(
        Season,
        verbose_name=_('Temporada'),
        on_delete=models.CASCADE,
        related_name='matches'
    )

    home_team = models.ForeignKey(
        Team,
        verbose_name=_('Equipo local'),
        on_delete=models.CASCADE,
        related_name='home_matches'
    )

    away_team = models.ForeignKey(
        Rival,
        verbose_name=_('Equipo visitante'),
        on_delete=models.CASCADE,
        related_name='away_matches',
        help_text=_('Equipo rival')
    )

    match_date = models.DateTimeField(
        _('Fecha y hora del partido'),
        help_text=_('Fecha y hora programada para el partido')
    )

    venue = models.CharField(
        _('Estadio/Campo'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_('Nombre del estadio o campo donde se juega')
    )

    match_type = models.CharField(
        _('Tipo de partido'),
        max_length=20,
        choices=MATCH_TYPE_CHOICES,
        default='friendly'
    )

    status = models.CharField(
        _('Estado'),
        max_length=20,
        choices=MATCH_STATUS_CHOICES,
        default='scheduled'
    )

    home_score = models.PositiveIntegerField(
        _('Goles equipo local'),
        null=True,
        blank=True,
        help_text=_('Goles marcados por el equipo local')
    )

    away_score = models.PositiveIntegerField(
        _('Goles equipo visitante'),
        null=True,
        blank=True,
        help_text=_('Goles marcados por el equipo visitante')
    )

    notes = models.TextField(
        _('Notas'),
        blank=True,
        null=True,
        help_text=_('Observaciones adicionales sobre el partido')
    )

    is_home = models.BooleanField(
        _('Partido en casa'),
        default=True,
        help_text=_('Indica si el partido se juega en casa o fuera')
    )

    class Meta:
        verbose_name = _('Partido')
        verbose_name_plural = _('Partidos')
        ordering = ['-match_date']

    def __str__(self):
        match_date_str = self.match_date.strftime('%d/%m/%Y %H:%M') if self.match_date else ''  # pylint: disable=no-member
        if self.is_home:
            return f"{self.home_team.name} vs {self.away_team.name} - {match_date_str}"
        else:
            return f"{self.away_team.name} vs {self.home_team.name} - {match_date_str}"

    def clean(self):
        """Validaciones personalizadas"""
        if self.status == 'finished':
            if self.home_score is None or self.away_score is None:
                raise ValidationError(_('Un partido finalizado debe tener marcador'))

    def save(self, *args, **kwargs):
        """
        Al guardar el partido, se asigna automáticamente a la temporada activa
        """
        if not self.season:
            active_season = Season.get_active()
            if active_season:
                self.season = active_season
            else:
                raise ValidationError(_('No hay una temporada activa. Debe crear y activar una temporada antes de crear partidos.'))

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def result(self):
        """Retorna el resultado del partido en formato texto"""
        if self.status == 'finished' and self.home_score is not None and self.away_score is not None:
            if self.is_home:
                return f"{self.home_score} - {self.away_score}"
            else:
                return f"{self.away_score} - {self.home_score}"
        return _('Sin resultado')

    @property
    def match_result_status(self):
        """Retorna si fue victoria, empate o derrota"""
        if self.status == 'finished' and self.home_score is not None and self.away_score is not None:
            if self.is_home:
                if self.home_score > self.away_score:
                    return 'victory'
                elif self.home_score < self.away_score:
                    return 'defeat'
                else:
                    return 'draw'
            else:
                if self.away_score > self.home_score:
                    return 'victory'
                elif self.away_score < self.home_score:
                    return 'defeat'
                else:
                    return 'draw'
        return 'pending'

    @property
    def is_finished(self):
        """Verifica si el partido ha terminado"""
        return self.status == 'finished'

    @property
    def is_upcoming(self):
        """Verifica si el partido está programado para el futuro"""
        return self.status == 'scheduled' and self.match_date > timezone.now()

    @property
    def days_until_match(self):
        """Retorna los días que faltan para el partido"""
        if self.match_date and self.match_date > timezone.now():
            return (self.match_date.date() - timezone.now().date()).days  # pylint: disable=no-member
        return 0
