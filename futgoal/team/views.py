from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from .models import Team

class TeamListView(ListView):
    model = Team
    template_name = 'team/team_list.html'
    context_object_name = 'teams'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Equipos')
        context['search_placeholder'] = _('Buscar equipos...')
        context['action_button'] = render_to_string('team/partials/team_create_button.html')
        context['breadcrumb_items'] = [
            {'name': _('Equipos'), 'url': reverse('team:list')}
        ]
        return context

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'team/TeamDetail.html'
    context_object_name = 'team'

    def get_object(self, queryset=None):
        return Team.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Detalles del Equipo')
        context['breadcrums'] = [
            {'title': _('Equipo')}
        ]
        return context

class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = 'team/TeamForm.html'
    context_object_name = 'team'
    fields = ['name', 'description', 'logo', 'coach', 'city', 'country', 'foundation_date', 'website']

    def get_object(self, queryset=None):
        return Team.objects.first()

    def get_success_url(self):
        return reverse('team:detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Editar Equipo')
        context['breadcrums'] = [
            {'title': _('Equipo'), 'url': reverse_lazy('team:detail')},
            {'title': _('Editar')}
        ]
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Equipo actualizado correctamente'))
        return response
