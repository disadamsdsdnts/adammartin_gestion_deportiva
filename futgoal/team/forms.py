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
