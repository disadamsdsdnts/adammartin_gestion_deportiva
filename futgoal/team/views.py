from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from .models import Team
from .forms import TeamUpdateForm

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
        context['breadcrumbs'] = [
            {'title': _('Equipo')}
        ]
        return context

class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = 'team/TeamForm.html'
    context_object_name = 'team'
    form_class = TeamUpdateForm

    def get_object(self, queryset=None):
        return Team.get_or_create_team()

    def get_success_url(self):
        # Verificar si viene de una configuración inicial
        is_initial_setup = self.request.GET.get('setup') == 'initial'

        if is_initial_setup:
            return reverse('dashboard')
        else:
            return reverse('team:detail')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Verificar si es configuración inicial
        is_initial_setup = self.request.GET.get('setup') == 'initial'
        team = self.get_object()

        if is_initial_setup or not team.name or not team.name.strip():
            kwargs['is_initial_setup'] = True

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Verificar si es configuración inicial
        is_initial_setup = self.request.GET.get('setup') == 'initial'
        team = self.get_object()

        if is_initial_setup or not team.name or not team.name.strip():
            context['page_title'] = _('Configuración inicial del equipo')
            context['breadcrumbs'] = [
                {'title': _('Configuración inicial')}
            ]
            context['is_initial_setup'] = True
        else:
            context['page_title'] = _('Editar Equipo')
            context['breadcrumbs'] = [
                {'title': _('Equipo'), 'url': reverse_lazy('team:detail')},
                {'title': _('Editar')}
            ]
            context['is_initial_setup'] = False

        return context

    def form_valid(self, form):
        # Verificar si es configuración inicial antes de guardar
        is_initial_setup = not self.object.name or not self.object.name.strip()

        response = super().form_valid(form)

        if is_initial_setup:
            messages.success(
                self.request,
                _('¡Perfecto! Tu equipo ha sido configurado. ¡Bienvenido a la gestión deportiva!')
            )
        else:
            messages.success(self.request, _('Equipo actualizado correctamente'))

        return response
