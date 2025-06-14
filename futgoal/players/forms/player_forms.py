from django import forms
from django.utils.translation import gettext_lazy as _

from ..models.player import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'identity_document',
            'sport_name',
            'email',
            'phone',
            'position',
            'dorsal',
            'country',
            'address',
            'city',
            'municipality',
            'postal_code',
            'region',
            'photo',
            'is_active'
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Nombre del jugador')
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Apellido del jugador')
                }
            ),
            'birth_date': forms.DateInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'type': 'date'
                }
            ),
            'identity_document': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Documento de identidad del jugador')
                }
            ),
            'sport_name': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Nombre deportivo del jugador')
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Email del jugador')
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Teléfono del jugador')
                }
            ),
            'position': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Posición del jugador')
                }
            ),
            'dorsal': forms.NumberInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Número de dorsal'),
                    'min': '1',
                    'max': '99'
                }
            ),
            'country': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('País del jugador')
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Dirección del jugador')
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Ciudad del jugador')
                }
            ),
            'municipality': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Municipio del jugador')
                }
            ),
            'postal_code': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Código postal del jugador')
                }
            ),
            'region': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Comunidad Autónoma del jugador')
                }
            ),
            'photo': forms.FileInput(
                attrs={
                    'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:focus:ring-primary-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600'
                }
            )
        }


class PlayerImportForm(forms.ModelForm):
    """Formulario simplificado para importación masiva de jugadores"""

    class Meta:
        model = Player
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'identity_document'
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Nombre'),
                    'required': True
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Apellidos'),
                    'required': True
                }
            ),
            'birth_date': forms.DateInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'type': 'date',
                    'required': True
                }
            ),
            'identity_document': forms.TextInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
                    'placeholder': _('Documento de identidad'),
                    'required': True
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer todos los campos obligatorios para importación
        for field_name in self.fields:
            self.fields[field_name].required = True

    def clean_identity_document(self):
        """Validar que el documento de identidad no esté duplicado"""
        identity_document = self.cleaned_data.get('identity_document')
        if identity_document:
            # Verificar si ya existe un jugador con este documento
            if Player.objects.filter(identity_document=identity_document).exists():
                raise forms.ValidationError(
                    _('Ya existe un jugador con este documento de identidad.')
                )
        return identity_document
