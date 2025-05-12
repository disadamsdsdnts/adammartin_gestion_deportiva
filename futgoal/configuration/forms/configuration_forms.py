from django.utils.translation import gettext as _
from django import forms
from django.forms import ModelForm
from futgoal.users.models.users import User

from futgoal.configuration.models.configuration import Configuration


class ConfigurationUpdateForm(ModelForm):
    class Meta:
        model = Configuration
        fields = [
            'app_name',
            'main_email',
            'enable_emails',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
