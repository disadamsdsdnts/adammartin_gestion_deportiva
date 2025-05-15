from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models

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
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(sport_name__icontains=search)
            )

        return queryset.order_by('first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Jugadores')
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse_lazy('dashboard')},
            {'title': _('Jugadores')}
        ]
        return context

class PlayerCreate(LoginRequiredMixin, CreateView):
    template_name = 'players/PlayerCreate.html'
    model = Player
    form_class = PlayerForm
    success_url = reverse_lazy('players:player_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Nuevo Jugador')
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse_lazy('dashboard')},
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
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse_lazy('dashboard')},
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
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse_lazy('dashboard')},
            {'title': _('Jugadores'), 'url': reverse_lazy('players:player_list')},
            {'title': _('Editar'), 'url': reverse_lazy('players:player_detail', kwargs={'pk': self.object.pk})},
            {'title': f"{self.object.first_name} {self.object.last_name}"}
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
        context['breadcrums'] = [
            {'title': _('Dashboard'), 'url': reverse_lazy('dashboard')},
            {'title': _('Jugadores'), 'url': reverse_lazy('players:player_list')},
            {'title': _('Eliminar')},
            {'title': f"{self.object.first_name} {self.object.last_name}"}
        ]
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Jugador eliminado correctamente'))
        return super().delete(request, *args, **kwargs)
