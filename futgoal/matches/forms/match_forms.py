from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from futgoal.matches.models import Match
from futgoal.season.models import Season
from futgoal.team.models import Team
from futgoal.rivals.models import Rival


class DateTimeLocalInput(forms.DateTimeInput):
    """
    Widget personalizado para datetime-local que maneja correctamente
    el formato de fecha tanto para valores iniciales como para errores de validación.
    """
    input_type = 'datetime-local'

    def format_value(self, value):
        if value is None:
            return ''

        # Si ya es una cadena (como cuando hay errores de validación), devolverla tal como está
        if isinstance(value, str):
            return value

        # Si es un objeto datetime, formatearlo para datetime-local
        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%dT%H:%M')

        return value


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
            'match_date': DateTimeLocalInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'required': True
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

        # Simplemente retornar la fecha sin validaciones de tiempo pasado
        # Esto permite crear partidos antiguos olvidados y editar partidos existentes
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


class MatchImportForm(forms.Form):
    """Formulario simplificado para importación masiva de partidos - No hereda de ModelForm para evitar validaciones del modelo"""

    ROLE_CHOICES = [
        ('1', _('Local')),
        ('0', _('Visitante'))
    ]

    TYPE_CHOICES = [
        ('friendly', _('Amistoso')),
        ('league', _('Liga')),
        ('cup', _('Copa')),
        ('playoff', _('Playoff')),
        ('training', _('Entrenamiento')),
    ]

    # Campo personalizado para el rol en el formulario de importación
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label=_('Rol'),
        help_text=_('Indica si el partido es local o visitante'),
        widget=forms.Select(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
            }
        )
    )

    # Campo personalizado para el nombre del equipo rival (texto libre)
    rival_name = forms.CharField(
        max_length=200,
        label=_('Equipo rival'),
        help_text=_('Nombre del equipo rival (se creará automáticamente si no existe)'),
        widget=forms.TextInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'placeholder': _('Ej: Barcelona FC, Real Madrid, etc.')
            }
        )
    )

    # Campos del partido
    match_date = forms.DateTimeField(
        label=_('Fecha y hora'),
        widget=forms.DateTimeInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'type': 'datetime-local'
            }
        )
    )

    match_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        label=_('Tipo de partido'),
        initial='friendly',
        widget=forms.Select(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
            }
        )
    )

    venue = forms.CharField(
        max_length=200,
        required=False,
        label=_('Lugar del partido'),
        widget=forms.TextInput(
            attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                'placeholder': _('Ej: Camp Nou, Santiago Bernabéu, etc.')
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Los labels ya están configurados en la definición de campos
        # Los valores por defecto ya están configurados en la definición de campos

    def clean_match_date(self):
        """Validación personalizada para la fecha del partido en importación"""
        match_date = self.cleaned_data.get('match_date')

        # En importación, permitimos fechas en el pasado
        # Se marcarán automáticamente como finalizados
        return match_date

    def clean(self):
        """Validaciones del formulario de importación"""
        cleaned_data = super().clean()

        # Verificar que hay una temporada activa
        if not Season.get_active():
            raise forms.ValidationError(
                _('No hay una temporada activa. Debe crear y activar una temporada antes de importar partidos.')
            )

        # Para importación, no validamos fechas en el pasado
        # Simplemente ajustamos el estado según la fecha
        match_date = cleaned_data.get('match_date')
        if match_date:
            from django.utils import timezone
            if match_date < timezone.now():
                # Si es en el pasado, marcar como finalizado automáticamente
                cleaned_data['status'] = 'finished'
            else:
                # Si es en el futuro, marcar como programado
                cleaned_data['status'] = 'scheduled'

        return cleaned_data

    def save(self, commit=True):
        """
        Crear y guardar el partido estableciendo automáticamente los campos requeridos
        """
        # Crear una nueva instancia de Match
        instance = Match()

        # Establecer los campos básicos desde el formulario
        instance.match_date = self.cleaned_data['match_date']
        instance.match_type = self.cleaned_data['match_type']
        instance.venue = self.cleaned_data.get('venue', '')

        # Obtener el equipo principal del sistema
        from futgoal.team.models import Team
        team = Team.objects.first()
        if not team:
            from django.core.exceptions import ValidationError
            raise forms.ValidationError(_('No hay un equipo creado. Debe crear un equipo antes de importar partidos.'))

        # Crear o buscar el equipo rival basado en el nombre
        rival_name = self.cleaned_data.get('rival_name')
        if rival_name:
            # Buscar equipo rival existente (insensible a mayúsculas/minúsculas)
            rival, created = Rival.objects.get_or_create(
                name__iexact=rival_name.strip(),
                defaults={'name': rival_name.strip()}
            )

            # Si se creó un nuevo rival, asociarlo con la temporada activa
            if created:
                active_season = Season.get_active()
                if active_season:
                    rival.seasons.add(active_season)

        # Establecer el rol (local/visitante)
        # En el modelo: home_team siempre es nuestro Team, away_team siempre es el Rival
        # is_home indica si jugamos en casa (True) o fuera (False)
        role = self.cleaned_data.get('role')
        instance.is_home = role == '1'  # '1' = Local (en casa), '0' = Visitante (fuera)
        instance.home_team = team  # Siempre nuestro equipo
        instance.away_team = rival  # Siempre el equipo rival

        # Establecer automáticamente la temporada activa
        if not instance.season_id:
            active_season = Season.get_active()
            if active_season:
                instance.season = active_season

        # Estado según la fecha del partido (ya se estableció en clean())
        # Si no se estableció en clean(), usar la lógica por defecto
        if not instance.status:
            from django.utils import timezone
            if instance.match_date and instance.match_date < timezone.now():
                # Si el partido es en el pasado, marcarlo como finalizado
                instance.status = 'finished'
            else:
                # Si el partido es en el futuro, marcarlo como programado
                instance.status = 'scheduled'

        if commit:
            # Para importación, deshabilitamos temporalmente la validación del modelo
            # que impide fechas en el pasado, ya que queremos permitirlas como partidos finalizados

            # Sobrescribir temporalmente el método clean del modelo
            original_clean = instance.clean

            def clean_import():
                """Validación modificada para importación que permite fechas pasadas"""
                from django.core.exceptions import ValidationError
                # Si el partido está finalizado, debe tener marcador (solo si se proporciona)
                if instance.status == 'finished':
                    if hasattr(instance, 'home_score') and hasattr(instance, 'away_score'):
                        if instance.home_score is not None and instance.away_score is not None:
                            pass  # Todo bien
                        elif instance.home_score is None and instance.away_score is None:
                            pass  # También está bien, partidos sin marcador
                        else:
                            raise ValidationError(_('Un partido finalizado debe tener marcador completo o ninguno'))
                # No validar fechas en el pasado para importación

            instance.clean = clean_import

            try:
                instance.save()
            finally:
                instance.clean = original_clean  # Restaurar validación original

        return instance


class MatchBulkUpdateForm(forms.Form):
    """Formulario para actualización masiva de partidos existentes"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        """Validaciones del formulario de actualización masiva"""
        cleaned_data = super().clean()

        # Verificar que hay una temporada activa
        if not Season.get_active():
            raise forms.ValidationError(
                _('No hay una temporada activa. Debe crear y activar una temporada antes de actualizar partidos.')
            )

        return cleaned_data

    def process_matches_data(self, matches_data):
        """
        Procesar y actualizar partidos existentes o crear nuevos
        """
        from futgoal.team.models import Team
        from django.utils import timezone
        from django.db import transaction

        # Función auxiliar para convertir scores a enteros
        def parse_score(score):
            """Convierte score a entero, manejando tanto enteros como floats"""
            if score is None:
                return None
            try:
                # Si ya es un entero, devolverlo directamente
                if isinstance(score, int):
                    return score
                # Si es float, convertir a entero
                if isinstance(score, float):
                    return int(score)
                # Si es string, intentar convertir
                if isinstance(score, str):
                    if not score.strip():
                        return None
                    float_score = float(score.strip())
                    return int(float_score)
                return None
            except (ValueError, TypeError):
                return None

        updated_matches = []
        created_matches = []
        errors = []

        # Obtener el equipo principal
        team = Team.objects.first()
        if not team:
            raise forms.ValidationError(_('No hay un equipo creado. Debe crear un equipo antes de actualizar partidos.'))

        active_season = Season.get_active()
        if not active_season:
            raise forms.ValidationError(_('No hay una temporada activa.'))

        with transaction.atomic():
            for index, match_data in enumerate(matches_data):
                try:
                    # Buscar partido existente por fecha, equipo rival y tipo
                    rival_name = match_data.get('rival_name', '').strip()
                    match_date_raw = match_data.get('match_date')
                    match_type = match_data.get('match_type', 'friendly')
                    is_home = match_data.get('is_home', True)

                    if not rival_name or not match_date_raw:
                        errors.append({
                            'row': index + 1,
                            'message': _('Datos incompletos: se requiere nombre del rival y fecha')
                        })
                        continue

                    # Convertir fecha de string a datetime si es necesario
                    if isinstance(match_date_raw, str):
                        from django.utils.dateparse import parse_datetime
                        match_date = parse_datetime(match_date_raw)
                        if not match_date:
                            errors.append({
                                'row': index + 1,
                                'message': _('Formato de fecha inválido')
                            })
                            continue
                    else:
                        match_date = match_date_raw

                    # Crear o obtener el rival
                    rival, created = Rival.objects.get_or_create(
                        name__iexact=rival_name,
                        defaults={'name': rival_name}
                    )

                    if created:
                        rival.seasons.add(active_season)

                    # Buscar partido existente con criterios específicos
                    # Buscamos por fecha (con tolerancia de 1 hora), rival y tipo
                    from datetime import timedelta
                    match_date_start = match_date - timedelta(hours=1)
                    match_date_end = match_date + timedelta(hours=1)

                    existing_match = Match.objects.filter(
                        season=active_season,
                        away_team=rival,
                        match_date__range=(match_date_start, match_date_end),
                        match_type=match_type
                    ).first()

                    if existing_match:
                        # Actualizar partido existente
                        existing_match.match_date = match_date
                        existing_match.venue = match_data.get('venue', existing_match.venue)
                        existing_match.is_home = is_home
                        existing_match.status = match_data.get('status', existing_match.status)

                        # Actualizar marcador si se proporciona
                        home_score = parse_score(match_data.get('home_score'))
                        away_score = parse_score(match_data.get('away_score'))
                        if home_score is not None and away_score is not None:
                            existing_match.home_score = home_score
                            existing_match.away_score = away_score
                            if existing_match.status == 'scheduled':
                                existing_match.status = 'finished'

                        existing_match.save()
                        updated_matches.append({
                            'id': existing_match.id,
                            'name': str(existing_match),
                            'action': 'updated'
                        })
                    else:
                        # Crear nuevo partido
                        new_match = Match(
                            season=active_season,
                            home_team=team,
                            away_team=rival,
                            match_date=match_date,
                            venue=match_data.get('venue', ''),
                            match_type=match_type,
                            is_home=is_home,
                            status=match_data.get('status', 'scheduled')
                        )

                        # Establecer marcador si se proporciona
                        home_score = parse_score(match_data.get('home_score'))
                        away_score = parse_score(match_data.get('away_score'))
                        if home_score is not None and away_score is not None:
                            new_match.home_score = home_score
                            new_match.away_score = away_score
                            if new_match.status == 'scheduled':
                                new_match.status = 'finished'

                        new_match.save()
                        created_matches.append({
                            'id': new_match.id,
                            'name': str(new_match),
                            'action': 'created'
                        })

                except Exception as e:
                    errors.append({
                        'row': index + 1,
                        'message': str(e)
                    })

        return {
            'updated': updated_matches,
            'created': created_matches,
            'errors': errors
        }
