from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from futgoal.matches.models import Match
from futgoal.season.models import Season
from futgoal.team.models import Team
from futgoal.rivals.models import Rival


class MatchForm(forms.ModelForm):
    """
    Formulario para crear y editar partidos.
    """

    class Meta:
        model = Match
        fields = [
            'home_team',
            'away_team',
            'match_date',
            'venue',
            'match_type',
            'status',
            'home_score',
            'away_score',
            'notes',
            'is_home'
        ]
        widgets = {
            'home_team': forms.HiddenInput(),
            'match_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'away_team': forms.Select(
                attrs={
                    'class': 'form-control form-select'
                }
            ),
            'venue': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Estadio o campo de juego')
                }
            ),
            'match_type': forms.Select(
                attrs={'class': 'form-control form-select'}
            ),
            'status': forms.Select(
                attrs={'class': 'form-control form-select'}
            ),
            'home_score': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'placeholder': _('Goles')
                }
            ),
            'away_score': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'placeholder': _('Goles')
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': _('Observaciones adicionales...')
                }
            ),
            'is_home': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalizar labels
        self.fields['away_team'].label = _('Equipo rival')
        self.fields['match_date'].label = _('Fecha y hora')
        self.fields['venue'].label = _('Estadio/Campo')
        self.fields['match_type'].label = _('Tipo de partido')
        self.fields['status'].label = _('Estado')
        self.fields['home_score'].label = _('Goles nuestro equipo')
        self.fields['away_score'].label = _('Goles equipo rival')
        self.fields['notes'].label = _('Notas')
        self.fields['is_home'].label = _('Partido en casa')

        # Configurar queryset para equipo rival
        active_season = Season.get_active()
        if active_season:
            self.fields['away_team'].queryset = Rival.objects.filter(seasons=active_season)
        else:
            self.fields['away_team'].queryset = Rival.objects.all()

        self.fields['away_team'].empty_label = _('Seleccionar equipo rival')

        # Configurar campos como no requeridos para ciertos casos
        self.fields['venue'].required = False
        self.fields['home_score'].required = False
        self.fields['away_score'].required = False
        self.fields['notes'].required = False

        # Establecer valor por defecto para tipo de partido
        if not self.instance.pk:  # Solo para nuevos partidos
            self.fields['match_type'].initial = 'friendly'

        # El campo home_team se establecerá automáticamente en save()
        self.fields['home_team'].required = False

    def clean_match_date(self):
        """Validar que la fecha del partido sea válida"""
        match_date = self.cleaned_data.get('match_date')
        status = self.cleaned_data.get('status', 'scheduled')

        if match_date and status == 'scheduled':
            # Solo validar para partidos programados
            if match_date < timezone.now():
                raise forms.ValidationError(
                    _('No se puede programar un partido en el pasado')
                )

        return match_date

    def clean(self):
        """Validaciones cruzadas del formulario"""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        home_score = cleaned_data.get('home_score')
        away_score = cleaned_data.get('away_score')

        # Si el partido está finalizado, debe tener marcador
        if status == 'finished':
            if home_score is None or away_score is None:
                raise forms.ValidationError(
                    _('Un partido finalizado debe tener el marcador completo')
                )

        # Verificar que hay una temporada activa
        if not Season.get_active():
            raise forms.ValidationError(
                _('No hay una temporada activa. Debe crear y activar una temporada antes de crear partidos.')
            )

        return cleaned_data

    def save(self, commit=True):
        """
        Guardar el partido estableciendo automáticamente el equipo local y temporada
        """
        instance = super().save(commit=False)

        # Establecer automáticamente la temporada activa si no está definida
        if not instance.season_id:
            active_season = Season.get_active()
            if active_season:
                instance.season = active_season
            else:
                from django.core.exceptions import ValidationError
                raise ValidationError(_('No hay una temporada activa. Debe crear y activar una temporada antes de crear partidos.'))

        # Establecer automáticamente el equipo local si no está definido
        if not instance.home_team_id:
            from futgoal.team.models import Team
            team = Team.objects.first()
            if team:
                instance.home_team = team
            else:
                from django.core.exceptions import ValidationError
                raise ValidationError(_('No hay un equipo creado. Debe crear un equipo antes de crear partidos.'))

        if commit:
            instance.save()
        return instance


class MatchFilterForm(forms.Form):
    """
    Formulario para filtrar la lista de partidos
    """

    STATUS_CHOICES = [('', _('Todos los estados'))] + Match.MATCH_STATUS_CHOICES
    TYPE_CHOICES = [('', _('Todos los tipos'))] + Match.MATCH_TYPE_CHOICES

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label=_('Estado'),
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )

    match_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
        label=_('Tipo'),
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )

    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        required=False,
        label=_('Temporada'),
        empty_label=_('Todas las temporadas'),
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )

    date_from = forms.DateField(
        required=False,
        label=_('Desde'),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )

    date_to = forms.DateField(
        required=False,
        label=_('Hasta'),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )
