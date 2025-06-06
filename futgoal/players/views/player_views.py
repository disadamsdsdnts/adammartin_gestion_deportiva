from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Q

from ..models.player import Player
from ..forms.player_forms import PlayerForm

class PlayerList(LoginRequiredMixin, ListView):
    template_name = 'players/PlayersList.html'
    model = Player
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(sport_name__icontains=search)
            )

        return queryset.order_by('first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Jugadores')
        context['breadcrumbs'] = [
            {'title': _('Jugadores')}
        ]
        context['action_button'] = f'<a href="{reverse_lazy("players:player_create")}" class="inline-flex items-center justify-center w-1/2 px-3 py-2 text-sm font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 sm:w-auto dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"><svg class="w-5 h-5 mr-2 -ml-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path></svg>{_("Añadir jugador")}</a>'
        return context

class PlayerCreate(LoginRequiredMixin, CreateView):
    template_name = 'players/PlayerCreate.html'
    model = Player
    form_class = PlayerForm
    success_url = reverse_lazy('players:player_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Nuevo Jugador')
        context['breadcrumbs'] = [
            {'title': _('Jugadores'), 'url': reverse_lazy('players:player_list')},
            {'title': _('Nuevo Jugador')}
        ]
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Jugador creado correctamente'))
        return response

class PlayerDetail(LoginRequiredMixin, DetailView):
    template_name = 'players/PlayerDetail.html'
    model = Player
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.object.first_name} {self.object.last_name}"
        context['breadcrumbs'] = [
            {'title': _('Jugadores'), 'url': reverse_lazy('players:player_list')},
            {'title': f"{self.object.first_name} {self.object.last_name}"}
        ]
        return context

class PlayerUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'players/PlayerUpdate.html'
    model = Player
    form_class = PlayerForm
    context_object_name = 'player'

    def get_success_url(self):
        return reverse_lazy('players:player_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Editar Jugador')
        context['breadcrumbs'] = [
            {'title': _('Jugadores'), 'url': reverse_lazy('players:player_list')},
            {'title': f"{self.object.first_name} {self.object.last_name}", 'url': reverse_lazy('players:player_detail', kwargs={'pk': self.object.pk})},
            {'title': _('Editar')}
        ]
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Jugador actualizado correctamente'))
        return response

class PlayerDelete(LoginRequiredMixin, DeleteView):
    model = Player
    success_url = reverse_lazy('players:player_list')
    template_name = '_includes/_base_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Eliminar Jugador')
        context['breadcrumbs'] = [
            {'title': _('Jugadores'), 'url': reverse_lazy('players:player_list')},
            {'title': f"{self.object.first_name} {self.object.last_name}", 'url': reverse_lazy('players:player_detail', kwargs={'pk': self.object.pk})},
            {'title': _('Eliminar')}
        ]
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Jugador eliminado correctamente'))
        return super().delete(request, *args, **kwargs)
