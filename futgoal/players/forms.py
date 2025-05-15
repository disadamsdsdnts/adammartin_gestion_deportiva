from django import forms
from django.utils.translation import gettext_lazy as _

from futgoal.players.models import Player


class PlayerForm(forms.ModelForm):
    """Formulario para crear y editar jugadores."""
    class Meta:
        model = Player
        fields = [
            'first_name', 'last_name', 'identity_document', 'sport_name',
            'email', 'phone', 'photo', 'position', 'country', 'biography',
            'address', 'city', 'municipality', 'postal_code', 'is_active'
        ]
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'municipality': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
