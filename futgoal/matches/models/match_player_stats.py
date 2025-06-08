from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from futgoal.utils.models import AuditModel
from futgoal.players.models import Player
from .match import Match


class MatchPlayerStats(AuditModel):
    """
    Modelo que representa las estadísticas individuales de un jugador en un partido específico.
    Actúa como tabla intermedia entre Match y Player con información adicional.
    """

    match = models.ForeignKey(
        Match,
        verbose_name=_('Partido'),
        on_delete=models.CASCADE,
        related_name='player_stats'
    )

    player = models.ForeignKey(
        Player,
        verbose_name=_('Jugador'),
        on_delete=models.CASCADE,
        related_name='match_stats'
    )

    # Estadísticas de goles y asistencias
    goals = models.PositiveIntegerField(
        _('Goles'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text=_('Número de goles marcados por el jugador en este partido')
    )

    assists = models.PositiveIntegerField(
        _('Asistencias'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text=_('Número de asistencias realizadas por el jugador en este partido')
    )

    # Tarjetas disciplinarias
    yellow_cards = models.PositiveIntegerField(
        _('Tarjetas amarillas'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Número de tarjetas amarillas recibidas')
    )

    red_cards = models.PositiveIntegerField(
        _('Tarjetas rojas'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_('Número de tarjetas rojas recibidas (0 o 1)')
    )

    # Tiempo de juego
    minutes_played = models.PositiveIntegerField(
        _('Minutos jugados'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        help_text=_('Minutos jugados en el partido (incluyendo tiempo extra)')
    )

    # Estado del jugador en el partido
    PLAYER_STATUS_CHOICES = [
        ('starter', _('Titular')),
        ('substitute', _('Suplente')),
        ('bench', _('En el banquillo')),
        ('not_available', _('No disponible')),
    ]

    status = models.CharField(
        _('Estado en el partido'),
        max_length=20,
        choices=PLAYER_STATUS_CHOICES,
        default='bench',
        help_text=_('Estado del jugador durante el partido')
    )

    # Minuto de sustitución
    substitution_in = models.PositiveIntegerField(
        _('Minuto de entrada'),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        help_text=_('Minuto en el que el jugador entró al campo')
    )

    substitution_out = models.PositiveIntegerField(
        _('Minuto de salida'),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        help_text=_('Minuto en el que el jugador salió del campo')
    )

    # Observaciones específicas del rendimiento
    performance_notes = models.TextField(
        _('Notas de rendimiento'),
        blank=True,
        null=True,
        help_text=_('Observaciones específicas sobre el rendimiento del jugador en este partido')
    )

    # Calificación del rendimiento (opcional)
    rating = models.DecimalField(
        _('Calificación'),
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text=_('Calificación del rendimiento del jugador (0-10)')
    )

    # Campo de asistencia al partido
    attended = models.BooleanField(
        _('Asistió al partido'),
        default=True,
        help_text=_('Indica si el jugador asistió al partido')
    )

    class Meta:
        verbose_name = _('Estadística de Jugador en Partido')
        verbose_name_plural = _('Estadísticas de Jugadores en Partidos')
        ordering = ['-match__match_date', 'player__sport_name']
        unique_together = ('match', 'player')  # Un jugador solo puede tener una entrada por partido

    def __str__(self):
        return f"{self.player.full_name} - {self.match} ({self.goals}G, {self.assists}A)"

    def clean(self):
        """Validaciones personalizadas"""
        from django.core.exceptions import ValidationError

        # Validar que las tarjetas rojas no excedan 1
        if self.red_cards > 1:
            raise ValidationError(_('Un jugador no puede recibir más de una tarjeta roja por partido'))

        # Validar que las tarjetas amarillas no excedan 2
        if self.yellow_cards > 2:
            raise ValidationError(_('Un jugador no puede recibir más de dos tarjetas amarillas por partido'))

        # Si recibe tarjeta roja, no puede recibir más de 1 amarilla
        if self.red_cards == 1 and self.yellow_cards > 1:
            raise ValidationError(_('Un jugador con tarjeta roja no puede tener más de una amarilla'))

        # Validar minutos de sustitución
        if self.substitution_in and self.substitution_out:
            if self.substitution_in >= self.substitution_out:
                raise ValidationError(_('El minuto de entrada debe ser menor al minuto de salida'))

        # Si está en el banquillo, no debería tener estadísticas de juego
        if self.status == 'bench' and (self.minutes_played > 0 or self.goals > 0 or self.assists > 0):
            raise ValidationError(_('Un jugador en el banquillo no puede tener estadísticas de juego'))

        # Si no está disponible, no debería tener ninguna estadística
        if self.status == 'not_available' and (
            self.minutes_played > 0 or self.goals > 0 or self.assists > 0 or
            self.yellow_cards > 0 or self.red_cards > 0
        ):
            raise ValidationError(_('Un jugador no disponible no puede tener estadísticas'))

        # Si no asistió al partido, no debería tener estadísticas de juego
        if not self.attended and (
            self.minutes_played > 0 or self.goals > 0 or self.assists > 0 or
            self.yellow_cards > 0 or self.red_cards > 0 or
            self.substitution_in is not None or self.substitution_out is not None
        ):
            raise ValidationError(_('Un jugador que no asistió al partido no puede tener estadísticas de juego'))

    @property
    def total_cards(self):
        """Retorna el total de tarjetas recibidas"""
        return self.yellow_cards + self.red_cards

    @property
    def has_disciplinary_action(self):
        """Verifica si el jugador recibió alguna tarjeta"""
        return self.yellow_cards > 0 or self.red_cards > 0

    @property
    def was_substituted(self):
        """Verifica si el jugador fue sustituido"""
        return self.substitution_out is not None

    @property
    def came_as_substitute(self):
        """Verifica si el jugador entró como sustituto"""
        return self.substitution_in is not None

    @property
    def played_full_match(self):
        """Verifica si el jugador jugó todo el partido (considerando 90 minutos como completo)"""
        return self.minutes_played >= 90 and not self.was_substituted

    @property
    def attended_match(self):
        """Verifica si el jugador asistió al partido"""
        return self.attended

    def get_performance_summary(self):
        """Retorna un resumen del rendimiento del jugador"""
        summary = []

        if self.goals > 0:
            summary.append(f"{self.goals} gol{'es' if self.goals > 1 else ''}")

        if self.assists > 0:
            summary.append(f"{self.assists} asistencia{'s' if self.assists > 1 else ''}")

        if self.yellow_cards > 0:
            summary.append(f"{self.yellow_cards} tarjeta{'s' if self.yellow_cards > 1 else ''} amarilla{'s' if self.yellow_cards > 1 else ''}")

        if self.red_cards > 0:
            summary.append("tarjeta roja")

        if not summary:
            return _("Sin estadísticas destacadas")

        return ", ".join(summary)
