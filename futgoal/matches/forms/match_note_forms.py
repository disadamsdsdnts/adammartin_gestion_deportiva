from django import forms
from django.utils.translation import gettext_lazy as _

from futgoal.matches.models import MatchNote


class MatchNoteForm(forms.ModelForm):
    """
    Formulario para crear y editar notas de partido
    """

    class Meta:
        model = MatchNote
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        self.match = kwargs.pop('match', None)
        super().__init__(*args, **kwargs)

        # Configurar widgets
        self.fields['title'].widget = forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': _('Título de la nota')
        })

        self.fields['content'].widget = forms.Textarea(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'rows': 4,
            'placeholder': _('Contenido detallado de la nota')
        })

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.match:
            instance.match = self.match
        if commit:
            instance.save()
        return instance
