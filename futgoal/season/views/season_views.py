from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from futgoal.season.models import Season
from futgoal.season.forms import SeasonForm

# Aquí se agregarán las vistas de la aplicación

class SeasonListView(LoginRequiredMixin, ListView):
    model = Season
    template_name = 'season/SeasonsList.html'
    context_object_name = 'object_list'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Temporadas')
        context['breadcrumbs'] = [
            {'title': _('Temporadas')}
        ]
        context['action_button'] = f'<a href="{reverse_lazy("season:season_create")}" class="inline-flex items-center justify-center w-1/2 px-3 py-2 text-sm font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 sm:w-auto dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"><svg class="w-5 h-5 mr-2 -ml-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path></svg>{_("Nueva Temporada")}</a>'
        return context

class SeasonCreateView(LoginRequiredMixin, CreateView):
    model = Season
    form_class = SeasonForm
    template_name = 'season/SeasonCreate.html'
    success_url = reverse_lazy('season:season_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Nueva Temporada')
        context['breadcrumbs'] = [
            {'title': _('Temporadas'), 'url': reverse_lazy('season:season_list')},
            {'title': _('Nueva Temporada')}
        ]
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Temporada creada exitosamente'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Error al crear la temporada'))
        return super().form_invalid(form)

class SeasonDetailView(LoginRequiredMixin, DetailView):
    model = Season
    template_name = 'season/SeasonDetail.html'
    context_object_name = 'season'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.name
        context['breadcrumbs'] = [
            {'title': _('Temporadas'), 'url': reverse_lazy('season:season_list')},
            {'title': self.object.name}
        ]
        return context

class SeasonUpdateView(LoginRequiredMixin, UpdateView):
    model = Season
    form_class = SeasonForm
    template_name = 'season/SeasonUpdate.html'
    context_object_name = 'season'

    def get_success_url(self):
        return reverse_lazy('season:season_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Editar Temporada')
        context['breadcrumbs'] = [
            {'title': _('Temporadas'), 'url': reverse_lazy('season:season_list')},
            {'title': self.object.name, 'url': reverse_lazy('season:season_detail', kwargs={'pk': self.object.pk})},
            {'title': _('Editar')}
        ]
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Temporada actualizada exitosamente'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Error al actualizar la temporada'))
        return super().form_invalid(form)

class SeasonDeleteView(LoginRequiredMixin, DeleteView):
    model = Season
    template_name = 'season/SeasonDetail.html'
    success_url = reverse_lazy('season:season_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Eliminar Temporada')
        context['breadcrumbs'] = [
            {'title': _('Temporadas'), 'url': reverse_lazy('season:season_list')},
            {'title': self.object.name, 'url': reverse_lazy('season:season_detail', kwargs={'pk': self.object.pk})},
            {'title': _('Eliminar')}
        ]
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Temporada eliminada exitosamente'))
        return super().delete(request, *args, **kwargs)
