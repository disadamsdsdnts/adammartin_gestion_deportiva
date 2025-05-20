from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class PlayerListView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Jugadores')
        context['search_placeholder'] = _('Buscar jugadores...')
        context['action_button'] = render_to_string('players/partials/player_create_button.html')
        context['breadcrumb_items'] = [
            {'name': _('Jugadores'), 'url': reverse('players:list')}
        ]
        return context

class PlayerDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Detalles del Jugador')
        context['action_button'] = render_to_string('players/partials/player_edit_button.html', {'player': self.object})
        context['breadcrumb_items'] = [
            {'name': _('Jugadores'), 'url': reverse('players:list')},
            {'name': self.object.name, 'url': reverse('players:detail', kwargs={'pk': self.object.pk})}
        ]
        return context

class PlayerCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Nuevo Jugador')
        context['breadcrumb_items'] = [
            {'name': _('Jugadores'), 'url': reverse('players:list')},
            {'name': _('Nuevo'), 'url': reverse('players:create')}
        ]
        return context

class PlayerUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Editar Jugador')
        context['breadcrumb_items'] = [
            {'name': _('Jugadores'), 'url': reverse('players:list')},
            {'name': self.object.name, 'url': reverse('players:detail', kwargs={'pk': self.object.pk})},
            {'name': _('Editar'), 'url': reverse('players:update', kwargs={'pk': self.object.pk})}
        ]
        return context
