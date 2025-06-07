from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Team


class TeamUpdateForm(forms.ModelForm):
    """Formulario para actualizar los datos del equipo."""

    class Meta:
        model = Team
        fields = [
            'name',
            'logo',
            'city',
            'country',
            'foundation_date',
            'coach',
            'description',
            'website',
        ]
        widgets = {
            'foundation_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.is_initial_setup = kwargs.pop('is_initial_setup', False)
        super().__init__(*args, **kwargs)

        # Si es configuración inicial, hacer el nombre obligatorio
        if self.is_initial_setup:
            self.fields['name'].required = True
            self.fields['name'].widget.attrs.update({
                'placeholder': _('Ej: Club Deportivo Los Campeones, FC Barcelona, etc.'),
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 font-medium'
            })

        # Mejorar labels y placeholders
        self.fields['name'].label = _('Nombre del equipo')
        self.fields['coach'].label = _('Entrenador')
        self.fields['city'].label = _('Ciudad')
        self.fields['country'].label = _('País')
        self.fields['foundation_date'].label = _('Fecha de fundación')
        self.fields['description'].label = _('Descripción')
        self.fields['website'].label = _('Sitio web')
        self.fields['logo'].label = _('Escudo del equipo')
