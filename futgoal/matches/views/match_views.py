from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Q

from futgoal.users.decorators import is_global_admin
from futgoal.matches.models import Match
from futgoal.matches.forms import MatchForm, MatchFilterForm


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchListView(ListView):
    """Vista para listar partidos"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        queryset = Match.objects.select_related('season', 'home_team').all()

        # Aplicar filtros si existen
        status = self.request.GET.get('status')
        match_type = self.request.GET.get('match_type')
        season = self.request.GET.get('season')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if status:
            queryset = queryset.filter(status=status)

        if match_type:
            queryset = queryset.filter(match_type=match_type)

        if season:
            queryset = queryset.filter(season_id=season)

        if date_from:
            queryset = queryset.filter(match_date__date__gte=date_from)

        if date_to:
            queryset = queryset.filter(match_date__date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = _('Partidos')
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
        ]
        context['actions'] = [
            {
                'title': _('Nuevo Partido'),
                'url': reverse('matches:match_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]

        # Añadir formulario de filtros
        context['filter_form'] = MatchFilterForm(self.request.GET)

        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchDetailView(DetailView):
    """Vista para ver detalle de un partido"""
    template_name = 'matches/MatchDetail.html'
    model = Match
    context_object_name = 'match'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = f"{_('Partido')}: {self.object}"
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': str(self.object)}
        ]
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('matches:match_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
            {
                'title': _('Eliminar'),
                'url': reverse('matches:match_delete', kwargs={'pk': self.object.pk}),
                'danger': True,
                'icon': '<i class="bi bi-trash"></i>'
            },
        ]
        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchCreateView(CreateView):
    """Vista para crear un nuevo partido"""
    template_name = 'matches/MatchCreate.html'
    model = Match
    form_class = MatchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = _('Nuevo Partido')
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Nuevo'), 'url': reverse('matches:match_create')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Partido creado correctamente')
        )
        return reverse_lazy('matches:match_detail', kwargs={'pk': self.object.pk})


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchUpdateView(UpdateView):
    """Vista para editar un partido"""
    template_name = 'matches/MatchUpdate.html'
    model = Match
    form_class = MatchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = _('Editar Partido')
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Editar')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Partido modificado correctamente')
        )
        return reverse_lazy('matches:match_detail', kwargs={'pk': self.object.pk})


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchDeleteView(DeleteView):
    """Vista para eliminar un partido"""
    model = Match
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = _("Eliminar Partido")
        context['breadcrumbs'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Eliminar')},
        ]
        context['delete_message'] = _('¿Está seguro de que desea eliminar el partido "{}"?').format(self.object)
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Partido eliminado correctamente')
        )
        return reverse_lazy('matches:match_list')
