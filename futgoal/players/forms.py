from django import forms
from django.utils.translation import gettext_lazy as _

from futgoal.players.models import Player


class PlayerForm(forms.ModelForm):
    """Formulario para crear y editar jugadores."""
    class Meta:
        model = Player
        fields = [
            'first_name', 'last_name', 'identity_document', 'sport_name',
            'email', 'phone', 'photo', 'position', 'country',
            'address', 'city', 'municipality', 'postal_code', 'is_active'
        ]
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'municipality': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clases de Tailwind a todos los campos
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
                })
            else:
                field.widget.attrs.update({
                    'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
                })

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name:
            self.add_error('first_name', _('El nombre es obligatorio'))
        if not last_name:
            self.add_error('last_name', _('Los apellidos son obligatorios'))

        return cleaned_data
