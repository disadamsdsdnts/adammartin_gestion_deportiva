from io import BytesIO
import re
import datetime


from django.views.generic import (
    FormView,
    DetailView,
    UpdateView,
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from futgoal.configuration.forms import ConfigurationUpdateForm
from futgoal.configuration.models import Configuration

from futgoal.users.decorators import is_global_admin


@method_decorator([is_global_admin, ], name='dispatch')
class ConfigurationDetailView(DetailView):
    model = Configuration
    template_name = 'configuration/ConfigurationDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Configuración'), 'url': reverse('configuration:configuration_list')},
        ]
        context['page_title'] = _('Configuración')
        context['breadcrumbs'] = breadcrumbs
        return context

    def get_object(self):
        return Configuration.objects.first()


@method_decorator([is_global_admin, ], name='dispatch')
class ConfigurationUpdateView(UpdateView):
    form_class = ConfigurationUpdateForm
    model = Configuration
    template_name = 'configuration/ConfigurationUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Configuración'), 'url': reverse('configuration:configuration_list')},
            {'title': _('Editar configuración')},
        ]
        context['page_title'] = _('Editar configuración')
        context['breadcrumbs'] = breadcrumbs
        return context

    def get_object(self):
        return Configuration.objects.first()

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Configuración actualizada correctamente')
        )
        return reverse_lazy(
            'configuration:configuration_detail'
        )
