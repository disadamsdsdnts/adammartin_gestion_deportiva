from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Rival
from futgoal.season.models import Season


class RivalForm(forms.ModelForm):
    """Formulario para gestionar los datos de equipos rivales."""

    class Meta:
        model = Rival
        fields = [
            'name',
            'seasons',
            'coach_name',
            'field_name',
            'city',
            'coach_phone',
            'coach_email',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
            'coach_email': forms.EmailInput(),
            'coach_phone': forms.TextInput(attrs={'placeholder': _('Ej: +34 666 777 888')}),
            'seasons': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hacer el campo nombre obligatorio
        self.fields['name'].required = True

        # Pre-seleccionar la temporada activa si está creando un nuevo rival
        if not self.instance.pk:
            active_season = Season.get_active()
            if active_season:
                self.fields['seasons'].initial = [active_season.pk]


class ImportRivalsForm(forms.Form):
    """Formulario para importar rivales de otras temporadas."""

    source_season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        label=_('Temporada origen'),
        help_text=_('Selecciona la temporada de donde importar los rivales'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    rivals = forms.ModelMultipleChoiceField(
        queryset=Rival.objects.none(),
        label=_('Rivales a importar'),
        help_text=_('Selecciona los rivales que quieres importar'),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        target_season = kwargs.pop('target_season', None)
        super().__init__(*args, **kwargs)

        if target_season:
            # Excluir la temporada objetivo de las opciones
            self.fields['source_season'].queryset = Season.objects.exclude(id=target_season.id)

    def set_rivals_queryset(self, season):
        """Actualiza el queryset de rivales basado en la temporada seleccionada."""
        if season:
            self.fields['rivals'].queryset = Rival.get_by_season(season)
