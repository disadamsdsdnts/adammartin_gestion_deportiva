from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Rival


class RivalForm(forms.ModelForm):
    """Formulario para gestionar los datos de equipos rivales."""

    class Meta:
        model = Rival
        fields = [
            'name',
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hacer el campo nombre obligatorio
        self.fields['name'].required = True
