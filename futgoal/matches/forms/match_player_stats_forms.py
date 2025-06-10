from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory

from futgoal.matches.models import MatchPlayerStats
from futgoal.players.models import Player


class MatchPlayerStatsForm(forms.ModelForm):
    """
    Formulario para gestionar las estadísticas individuales de un jugador en un partido.
    """

    class Meta:
        model = MatchPlayerStats
        fields = [
            'player',
            'attended',
            'status',
            'minutes_played',
            'goals',
            'assists',
            'yellow_cards',
            'red_cards',
            'substitution_in',
            'substitution_out',
            'rating',
            'performance_notes'
        ]
        widgets = {
            'player': forms.Select(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
                }
            ),
            'attended': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
                }
            ),
            'minutes_played': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'min': '0',
                    'max': '120',
                    'placeholder': _('Minutos jugados')
                }
            ),
            'goals': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'min': '0',
                    'max': '20',
                    'placeholder': _('Goles')
                }
            ),
            'assists': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'min': '0',
                    'max': '20',
                    'placeholder': _('Asistencias')
                }
            ),
            'yellow_cards': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'min': '0',
                    'max': '2',
                    'placeholder': _('Tarjetas amarillas')
                }
            ),
            'red_cards': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'min': '0',
                    'max': '1',
                    'placeholder': _('Tarjetas rojas')
                }
            ),
            'substitution_in': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'min': '0',
                    'max': '120',
                    'placeholder': _('Minuto de entrada')
                }
            ),
            'substitution_out': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'min': '0',
                    'max': '120',
                    'placeholder': _('Minuto de salida')
                }
            ),
            'rating': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'min': '0',
                    'max': '10',
                    'step': '0.1',
                    'placeholder': _('Calificación (0-10)')
                }
            ),
            'performance_notes': forms.Textarea(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'rows': 3,
                    'placeholder': _('Observaciones sobre el rendimiento del jugador...')
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar solo jugadores activos
        self.fields['player'].queryset = Player.objects.filter(is_active=True).order_by('first_name', 'last_name')
        self.fields['player'].empty_label = _('Seleccionar jugador')

        # Hacer algunos campos opcionales para mejor UX
        self.fields['substitution_in'].required = False
        self.fields['substitution_out'].required = False
        self.fields['rating'].required = False
        self.fields['performance_notes'].required = False

    def clean(self):
        """Validaciones personalizadas del formulario"""
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        attended = cleaned_data.get('attended', True)
        minutes_played = cleaned_data.get('minutes_played', 0)
        goals = cleaned_data.get('goals', 0)
        assists = cleaned_data.get('assists', 0)
        yellow_cards = cleaned_data.get('yellow_cards', 0)
        red_cards = cleaned_data.get('red_cards', 0)
        substitution_in = cleaned_data.get('substitution_in')
        substitution_out = cleaned_data.get('substitution_out')

        # Validaciones según el estado del jugador
        if status == 'bench':
            if minutes_played > 0 or goals > 0 or assists > 0:
                raise forms.ValidationError(
                    _('Un jugador en el banquillo no puede tener estadísticas de juego')
                )

        if status == 'not_available':
            if any([minutes_played, goals, assists, yellow_cards, red_cards]):
                raise forms.ValidationError(
                    _('Un jugador no disponible no puede tener estadísticas')
                )

        # Validaciones según la asistencia
        if not attended:
            if any([minutes_played, goals, assists, yellow_cards, red_cards, substitution_in, substitution_out]):
                raise forms.ValidationError(
                    _('Un jugador que no asistió al partido no puede tener estadísticas de juego')
                )

        # Validar sustituciones
        if substitution_in and substitution_out:
            if substitution_in >= substitution_out:
                raise forms.ValidationError(
                    _('El minuto de entrada debe ser menor al minuto de salida')
                )

        # Si es titular y no tiene minuto de entrada, pero sí de salida, es válido
        # Si es suplente y tiene minuto de entrada, es válido
        if status == 'substitute' and not substitution_in and minutes_played > 0:
            raise forms.ValidationError(
                _('Un suplente que jugó debe tener especificado el minuto de entrada')
            )

        return cleaned_data


class MatchPlayerStatsBaseFormSet(forms.BaseFormSet):
    """
    FormSet base personalizado para las estadísticas de jugadores
    """

    def clean(self):
        """Validaciones a nivel de formset"""
        if any(self.errors):
            return

        players = []
        total_goals = 0

        for form in self.forms:
            if form.cleaned_data:
                player = form.cleaned_data.get('player')
                goals = form.cleaned_data.get('goals', 0)

                # Verificar que no haya jugadores duplicados
                if player and player in players:
                    raise forms.ValidationError(
                        _('No se puede agregar el mismo jugador múltiples veces')
                    )
                players.append(player)

                total_goals += goals

        # Podríamos agregar validaciones adicionales aquí
        # Por ejemplo, verificar que el total de goles no exceda el marcador del partido


# Crear el formset para múltiples jugadores
MatchPlayerStatsFormSet = formset_factory(
    MatchPlayerStatsForm,
    formset=MatchPlayerStatsBaseFormSet,
    extra=0,  # No queremos formularios extra en la gestión masiva
    can_delete=False  # No permitimos eliminar en la gestión masiva
)


class MatchPlayerStatsQuickForm(forms.ModelForm):
    """
    Formulario simplificado para agregar estadísticas rápidamente
    """

    class Meta:
        model = MatchPlayerStats
        fields = ['player', 'attended', 'status', 'minutes_played', 'goals', 'assists', 'yellow_cards', 'red_cards']
        widgets = {
            'player': forms.Select(attrs={'class': 'form-control'}),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'minutes_played': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '120'}),
            'goals': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '20'}),
            'assists': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '20'}),
            'yellow_cards': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '2'}),
            'red_cards': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.filter(is_active=True).order_by('first_name', 'last_name')
        self.fields['player'].empty_label = _('Seleccionar jugador')


class MatchPlayerStatsFilterForm(forms.Form):
    """
    Formulario para filtrar estadísticas de jugadores
    """

    player = forms.ModelChoiceField(
        queryset=Player.objects.filter(is_active=True).order_by('first_name', 'last_name'),
        required=False,
        empty_label=_('Todos los jugadores'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    SEASON_CHOICES = [
        ('', _('Todas las temporadas')),
        ('active', _('Temporada actual')),
    ]

    season = forms.ChoiceField(
        choices=SEASON_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    min_goals = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Goles mínimos')
        })
    )

    min_assists = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Asistencias mínimas')
        })
    )


class MatchPlayerStatsImportForm(forms.Form):
    """Formulario para importación masiva de estadísticas de jugadores desde CSV"""

    # Campo para el archivo CSV
    csv_file = forms.FileField(
        label=_('Archivo CSV'),
        help_text=_('Seleccione un archivo CSV con las estadísticas de jugadores'),
        widget=forms.FileInput(
            attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
                'accept': '.csv'
            }
        )
    )

    # Campos para cada estadística individual (para la tabla de previsualización)
    rival_name = forms.CharField(
        max_length=200,
        label=_('Rival'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'readonly': True
            }
        )
    )

    match_date = forms.CharField(
        label=_('Fecha y hora'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'readonly': True
            }
        )
    )

    player_name = forms.CharField(
        max_length=100,
        label=_('Nombre del jugador'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'placeholder': _('Nombre')
            }
        )
    )

    player_lastname = forms.CharField(
        max_length=100,
        label=_('Apellidos del jugador'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'placeholder': _('Apellidos')
            }
        )
    )

    goals = forms.IntegerField(
        label=_('Goles'),
        min_value=0,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'min': '0',
                'max': '20'
            }
        )
    )

    yellow_cards = forms.IntegerField(
        label=_('Tarjetas amarillas'),
        min_value=0,
        max_value=2,
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'min': '0',
                'max': '2'
            }
        )
    )

    red_cards = forms.IntegerField(
        label=_('Tarjetas rojas'),
        min_value=0,
        max_value=1,
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'min': '0',
                'max': '1'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Los campos de datos específicos no son requeridos para el formulario principal
        for field_name in ['rival_name', 'match_date', 'player_name', 'player_lastname', 'goals', 'yellow_cards', 'red_cards']:
            self.fields[field_name].required = False

    def clean_csv_file(self):
        """Validar el archivo CSV"""
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            # Verificar que sea un archivo CSV
            if not csv_file.name.endswith('.csv'):
                raise forms.ValidationError(_('El archivo debe ser un CSV (.csv)'))

            # Verificar tamaño del archivo (máximo 5MB)
            if csv_file.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError(_('El archivo es demasiado grande. Máximo permitido: 5MB'))

        return csv_file
