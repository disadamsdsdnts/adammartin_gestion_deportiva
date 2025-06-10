from django.shortcuts import render, get_object_or_404, redirect
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
    DeleteView,
    TemplateView
)
from django.db.models import Q, Sum, Avg, Count
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.forms import formset_factory

from futgoal.matches.models import Match, MatchPlayerStats
from futgoal.matches.forms.match_player_stats_forms import (
    MatchPlayerStatsForm,
    MatchPlayerStatsFormSet,
    MatchPlayerStatsQuickForm,
    MatchPlayerStatsFilterForm
)
from futgoal.players.models import Player
from futgoal.season.models import Season


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsListView(ListView):
    """Vista para listar todas las estadísticas de jugadores por partido"""
    template_name = 'matches/player_stats/MatchPlayerStatsList.html'
    model = MatchPlayerStats
    context_object_name = 'stats'
    paginate_by = 20

    def get_queryset(self):
        queryset = MatchPlayerStats.objects.select_related('match', 'player', 'match__season').order_by('-match__match_date')

        # Aplicar filtros
        form = MatchPlayerStatsFilterForm(self.request.GET)
        if form.is_valid():
            player = form.cleaned_data.get('player')
            season = form.cleaned_data.get('season')
            min_goals = form.cleaned_data.get('min_goals')
            min_assists = form.cleaned_data.get('min_assists')

            if player:
                queryset = queryset.filter(player=player)

            if season == 'active':
                active_season = Season.get_active()
                if active_season:
                    queryset = queryset.filter(match__season=active_season)

            if min_goals is not None:
                queryset = queryset.filter(goals__gte=min_goals)

            if min_assists is not None:
                queryset = queryset.filter(assists__gte=min_assists)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Estadísticas de Jugadores')
        context['breadcrumbs'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Estadísticas de Jugadores')},
        ]
        context['filter_form'] = MatchPlayerStatsFilterForm(self.request.GET)
        context['actions'] = [
            {
                'title': _('Ver Resumen'),
                'url': reverse('matches:player_stats_summary'),
                'primary': False,
                'icon': '<i class="bi bi-graph-up"></i>'
            },
        ]
        return context


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsDetailView(DetailView):
    """Vista para ver el detalle de estadísticas de un jugador en un partido"""
    template_name = 'matches/player_stats/MatchPlayerStatsDetail.html'
    model = MatchPlayerStats
    context_object_name = 'stat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{_('Estadísticas')} - {self.object.player.full_name}"
        context['breadcrumbs'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Estadísticas'), 'url': reverse('matches:player_stats_list')},
            {'title': self.object.player.full_name},
        ]
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('matches:player_stats_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]
        return context


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsCreateView(CreateView):
    """Vista para crear estadísticas de un jugador en un partido"""
    template_name = 'matches/player_stats/MatchPlayerStatsCreate.html'
    model = MatchPlayerStats
    form_class = MatchPlayerStatsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Si viene desde un partido específico
        match_id = self.request.GET.get('match_id')
        if match_id:
            match = get_object_or_404(Match, pk=match_id)
            context['match'] = match
            context['page_title'] = f"{_('Agregar Estadísticas')} - {match}"
        else:
            context['page_title'] = _('Agregar Estadísticas de Jugador')

        context['breadcrumbs'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Estadísticas'), 'url': reverse('matches:player_stats_list')},
            {'title': _('Agregar')},
        ]
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Si viene desde un partido específico, pre-seleccionar el partido
        match_id = self.request.GET.get('match_id')
        if match_id:
            match = get_object_or_404(Match, pk=match_id)
            form.instance.match = match

        return form

    def form_valid(self, form):
        # Asignar el partido si viene como parámetro
        match_id = self.request.GET.get('match_id')
        if match_id:
            form.instance.match = get_object_or_404(Match, pk=match_id)

        response = super().form_valid(form)
        messages.success(self.request, _('Estadísticas de jugador agregadas correctamente'))
        return response

    def get_success_url(self):
        return reverse_lazy('matches:player_stats_detail', kwargs={'pk': self.object.pk})


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsUpdateView(UpdateView):
    """Vista para editar estadísticas de un jugador en un partido"""
    template_name = 'matches/player_stats/MatchPlayerStatsUpdate.html'
    model = MatchPlayerStats
    form_class = MatchPlayerStatsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{_('Editar Estadísticas')} - {self.object.player.full_name}"
        context['breadcrumbs'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Estadísticas'), 'url': reverse('matches:player_stats_list')},
            {'title': self.object.player.full_name, 'url': reverse('matches:player_stats_detail', kwargs={'pk': self.object.pk})},
            {'title': _('Editar')},
        ]
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Estadísticas de jugador actualizadas correctamente'))
        return response

    def get_success_url(self):
        return reverse_lazy('matches:player_stats_detail', kwargs={'pk': self.object.pk})


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsDeleteView(DeleteView):
    """Vista para eliminar estadísticas de un jugador en un partido"""
    model = MatchPlayerStats
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{_('Eliminar Estadísticas')} - {self.object.player.full_name}"
        context['breadcrumbs'] = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Estadísticas'), 'url': reverse('matches:player_stats_list')},
            {'title': _('Eliminar')},
        ]
        return context

    def get_success_url(self):
        messages.success(self.request, _('Estadísticas de jugador eliminadas correctamente'))
        return reverse_lazy('matches:player_stats_list')


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsManageView(View):
    """Vista para gestionar todas las estadísticas de un partido específico"""
    template_name = 'matches/player_stats/MatchPlayerStatsManage.html'

    def get_context_data(self, match, formset):
        """Obtener contexto común para GET y POST"""
        context = {
            'match': match,
            'formset': formset,
            'page_title': f"{_('Gestionar Estadísticas')} - {match}",
            'breadcrumbs': [
                {'title': _('Dashboard'), 'url': reverse('dashboard')},
                {'title': _('Partidos'), 'url': reverse('matches:match_list')},
                {'title': str(match), 'url': reverse('matches:match_detail', kwargs={'pk': match.pk})},
                {'title': _('Gestionar Estadísticas')},
            ],
        }
        return context

    def get(self, request, *args, **kwargs):
        """Mostrar el formset para gestionar estadísticas"""
        match = get_object_or_404(Match, pk=kwargs['match_id'])

        # Obtener o crear estadísticas para todos los jugadores activos
        players = Player.objects.filter(is_active=True).order_by('first_name', 'last_name')

        # Crear datos iniciales para el formset
        initial_data = []
        for player in players:
            try:
                # Intentar obtener estadísticas existentes
                stats = MatchPlayerStats.objects.get(match=match, player=player)
                initial_data.append({
                    'player': player,
                    'attended': stats.attended,
                    'status': stats.status,
                    'minutes_played': stats.minutes_played,
                    'goals': stats.goals,
                    'assists': stats.assists,
                    'yellow_cards': stats.yellow_cards,
                    'red_cards': stats.red_cards,
                    'substitution_in': stats.substitution_in,
                    'substitution_out': stats.substitution_out,
                    'rating': stats.rating,
                    'performance_notes': stats.performance_notes,
                })
            except MatchPlayerStats.DoesNotExist:
                # Crear entrada con valores por defecto
                initial_data.append({
                    'player': player,
                    'attended': True,
                    'status': 'bench',
                    'minutes_played': 0,
                    'goals': 0,
                    'assists': 0,
                    'yellow_cards': 0,
                    'red_cards': 0,
                    'substitution_in': None,
                    'substitution_out': None,
                    'rating': None,
                    'performance_notes': '',
                })

        # Crear formset con datos iniciales
        formset = MatchPlayerStatsFormSet(initial=initial_data)

        # Asignar match a cada formulario
        for form, data in zip(formset.forms, initial_data):
            form.instance.player = data['player']
            form.instance.match = match

        context = self.get_context_data(match, formset)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Procesar el formset de estadísticas"""
        match = get_object_or_404(Match, pk=kwargs['match_id'])

        formset = MatchPlayerStatsFormSet(request.POST)

        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        player = form.cleaned_data['player']

                        # Actualizar o crear estadísticas
                        stats, created = MatchPlayerStats.objects.update_or_create(
                            match=match,
                            player=player,
                            defaults={
                                'attended': form.cleaned_data['attended'],
                                'status': form.cleaned_data['status'],
                                'minutes_played': form.cleaned_data['minutes_played'],
                                'goals': form.cleaned_data['goals'],
                                'assists': form.cleaned_data['assists'],
                                'yellow_cards': form.cleaned_data['yellow_cards'],
                                'red_cards': form.cleaned_data['red_cards'],
                                'substitution_in': form.cleaned_data.get('substitution_in'),
                                'substitution_out': form.cleaned_data.get('substitution_out'),
                                'rating': form.cleaned_data.get('rating'),
                                'performance_notes': form.cleaned_data.get('performance_notes', ''),
                            }
                        )

            messages.success(request, _('Estadísticas actualizadas correctamente'))
            return redirect('matches:match_detail', pk=match.pk)

        context = self.get_context_data(match, formset)
        return render(request, self.template_name, context)


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsSummaryView(TemplateView):
    """Vista para mostrar resumen y estadísticas globales de jugadores"""
    template_name = 'matches/player_stats/MatchPlayerStatsSummary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener temporada activa
        active_season = Season.get_active()

        if active_season:
            # Estadísticas de la temporada actual
            season_stats = MatchPlayerStats.objects.filter(match__season=active_season)
        else:
            # Si no hay temporada activa, usar todas las estadísticas
            season_stats = MatchPlayerStats.objects.all()

        # Top goleadores
        top_scorers = season_stats.values('player__first_name', 'player__last_name', 'player__sport_name', 'player__id').annotate(
            total_goals=Sum('goals'),
            matches_played=Count('match', distinct=True)
        ).filter(total_goals__gt=0).order_by('-total_goals')[:10]

        # Top asistentes
        top_assisters = season_stats.values('player__first_name', 'player__last_name', 'player__sport_name', 'player__id').annotate(
            total_assists=Sum('assists'),
            matches_played=Count('match', distinct=True)
        ).filter(total_assists__gt=0).order_by('-total_assists')[:10]

        # Jugadores con más tarjetas
        most_carded = season_stats.values('player__first_name', 'player__last_name', 'player__sport_name', 'player__id').annotate(
            total_yellow=Sum('yellow_cards'),
            total_red=Sum('red_cards'),
            total_cards=Sum('yellow_cards') + Sum('red_cards'),
            matches_played=Count('match', distinct=True)
        ).filter(total_cards__gt=0).order_by('-total_cards')[:10]

        # Jugadores con más minutos
        most_minutes = season_stats.values('player__first_name', 'player__last_name', 'player__sport_name', 'player__id').annotate(
            total_minutes=Sum('minutes_played'),
            matches_played=Count('match', distinct=True),
            avg_minutes=Avg('minutes_played')
        ).filter(total_minutes__gt=0).order_by('-total_minutes')[:10]

        # Estadísticas generales
        total_stats = season_stats.aggregate(
            total_goals=Sum('goals'),
            total_assists=Sum('assists'),
            total_yellow=Sum('yellow_cards'),
            total_red=Sum('red_cards'),
            total_minutes=Sum('minutes_played'),
            matches_with_stats=Count('match', distinct=True)
        )

        context.update({
            'page_title': _('Resumen de Estadísticas'),
            'breadcrumbs': [
                {'title': _('Dashboard'), 'url': reverse('dashboard')},
                {'title': _('Partidos'), 'url': reverse('matches:match_list')},
                {'title': _('Estadísticas'), 'url': reverse('matches:player_stats_list')},
                {'title': _('Resumen')},
            ],
            'active_season': active_season,
            'top_scorers': top_scorers,
            'top_assisters': top_assisters,
            'most_carded': most_carded,
            'most_minutes': most_minutes,
            'total_stats': total_stats,
        })

        return context


@method_decorator([login_required], name='dispatch')
class PlayerStatsHistoryView(DetailView):
    """Vista para ver el historial de estadísticas de un jugador específico"""
    template_name = 'matches/player_stats/PlayerStatsHistory.html'
    model = Player
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todas las estadísticas del jugador
        player_stats = MatchPlayerStats.objects.filter(player=self.object).select_related('match', 'match__season').order_by('-match__match_date')

        # Paginación
        paginator = Paginator(player_stats, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Estadísticas totales del jugador
        total_stats = player_stats.aggregate(
            total_goals=Sum('goals'),
            total_assists=Sum('assists'),
            total_yellow=Sum('yellow_cards'),
            total_red=Sum('red_cards'),
            total_minutes=Sum('minutes_played'),
            matches_played=Count('match'),
            avg_rating=Avg('rating')
        )

        # Estadísticas por temporada
        season_stats = player_stats.values('match__season__name').annotate(
            goals=Sum('goals'),
            assists=Sum('assists'),
            matches=Count('match'),
            minutes=Sum('minutes_played'),
            avg_rating=Avg('rating')
        ).order_by('-match__season__start_date')

        context.update({
            'page_title': f"{_('Historial de')} {self.object.full_name}",
            'breadcrumbs': [
                {'title': _('Dashboard'), 'url': reverse('dashboard')},
                {'title': _('Jugadores'), 'url': reverse('players:player_list')},
                {'title': self.object.full_name, 'url': reverse('players:player_detail', kwargs={'pk': self.object.pk})},
                {'title': _('Historial de Estadísticas')},
            ],
            'player_stats': page_obj,
            'total_stats': total_stats,
            'season_stats': season_stats,
        })

        return context


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsQuickAddView(View):
    """Vista AJAX para agregar estadísticas rápidamente"""

    def post(self, request, *args, **kwargs):
        match_id = request.POST.get('match_id')
        player_id = request.POST.get('player_id')

        if not match_id or not player_id:
            return JsonResponse({'success': False, 'error': _('Datos incompletos')})

        try:
            match = Match.objects.get(pk=match_id)
            player = Player.objects.get(pk=player_id)

            # Verificar que no exista ya
            if MatchPlayerStats.objects.filter(match=match, player=player).exists():
                return JsonResponse({'success': False, 'error': _('Ya existen estadísticas para este jugador en este partido')})

            # Crear estadísticas básicas
            stats = MatchPlayerStats.objects.create(
                match=match,
                player=player,
                status='bench'  # Estado por defecto
            )

            return JsonResponse({
                'success': True,
                'message': _('Estadísticas agregadas correctamente'),
                'stats_id': stats.pk,
                'redirect_url': reverse('matches:player_stats_update', kwargs={'pk': stats.pk})
            })

        except (Match.DoesNotExist, Player.DoesNotExist):
            return JsonResponse({'success': False, 'error': _('Partido o jugador no encontrado')})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
