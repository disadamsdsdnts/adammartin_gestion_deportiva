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
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from futgoal.matches.models import Match, MatchPlayerStats
from futgoal.matches.forms.match_player_stats_forms import (
    MatchPlayerStatsForm,
    MatchPlayerStatsFormSet,
    MatchPlayerStatsQuickForm,
    MatchPlayerStatsFilterForm,
    MatchPlayerStatsImportForm
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


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsImportView(View):
    """Vista para importar estadísticas de jugadores desde CSV"""
    template_name = 'matches/player_stats/MatchPlayerStatsImport.html'

    def get(self, request, *args, **kwargs):
        """Mostrar formulario de importación"""
        form = MatchPlayerStatsImportForm()
        context = {
            'form': form,
            'page_title': _('Importar Estadísticas'),
            'breadcrumbs': [

                {'title': _('Estadísticas'), 'url': reverse('matches:player_stats_list')},
                {'title': _('Importar')},
            ],
        }
        return render(request, self.template_name, context)


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsImportCSVTemplateView(View):
    """Vista para descargar plantilla CSV de importación de estadísticas"""

    def get(self, request, *args, **kwargs):
        """Generar y descargar plantilla CSV"""
        from django.http import HttpResponse
        import csv

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="plantilla_estadisticas_jugadores.csv"'

        # Añadir BOM para Excel
        response.write('\ufeff')

        writer = csv.writer(response)

        # Escribir headers basados en el CSV proporcionado
        writer.writerow([
            'Rival',
            'Fecha y hora',
            'Nombre',
            'Apellidos',
            'Goles',
            'Tarjetas rojas',
            'Tarjetas amarillas'
        ])

        # Escribir algunas filas de ejemplo
        writer.writerow([
            'LA POSTA CARCHUNA-CALAHONDA',
            '15-09-2024 09:00',
            'MARIO',
            'JURADO CASAS',
            '1',
            '0',
            '0'
        ])
        writer.writerow([
            'BARCELONA FC',
            '22-09-2024 16:30',
            'JUAN',
            'PÉREZ GARCÍA',
            '2',
            '0',
            '1'
        ])
        writer.writerow([
            'REAL MADRID',
            '29-09-2024 20:00',
            'CARLOS',
            'MARTÍN LÓPEZ',
            '0',
            '1',
            '0'
        ])

        return response


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsProcessCSVView(View):
    """Vista para procesar archivo CSV de estadísticas"""

    def post(self, request, *args, **kwargs):
        """Procesar archivo CSV y devolver datos para previsualización"""
        import csv
        import io
        from datetime import datetime
        from django.utils import timezone
        from zoneinfo import ZoneInfo

        # Configurar timezone de Madrid usando zoneinfo (Python 3.9+)
        madrid_tz = ZoneInfo('Europe/Madrid')

        # Obtener archivos CSV (puede ser uno o varios)
        csv_files = request.FILES.getlist('csv_files')
        if not csv_files:
            # Compatibilidad con version anterior de un solo archivo
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                csv_files = [csv_file]
            else:
                return JsonResponse({'success': False, 'error': _('No se seleccionó ningún archivo')})

        try:
            all_stats_to_process = []
            all_errors = []
            total_files_processed = 0

            for file_index, csv_file in enumerate(csv_files):
                file_name = csv_file.name

                # Validar tamaño del archivo
                if csv_file.size > 5 * 1024 * 1024:  # 5MB
                    all_errors.append(f"Archivo '{file_name}': Archivo demasiado grande (máximo 5MB)")
                    continue

                try:
                    # Leer el archivo CSV
                    decoded_file = csv_file.read().decode('utf-8-sig')  # utf-8-sig para manejar BOM
                    csv_data = csv.DictReader(io.StringIO(decoded_file))

                    stats_to_process = []
                    file_errors = []
                    row_number = 1  # Empezar desde 1 (header no cuenta)

                    for row in csv_data:
                        row_number += 1
                        row_errors = []

                        # Limpiar datos
                        rival_name = row.get('Rival', '').strip()
                        fecha_hora = row.get('Fecha y hora', '').strip()
                        nombre_jugador = row.get('Nombre', '').strip()
                        apellidos_jugador = row.get('Apellidos', '').strip()
                        goles = row.get('Goles', '0').strip()
                        tarjetas_rojas = row.get('Tarjetas rojas', '0').strip()
                        tarjetas_amarillas = row.get('Tarjetas amarillas', '0').strip()

                        # Validaciones básicas
                        if not rival_name:
                            row_errors.append(_('El nombre del rival es obligatorio'))

                        if not fecha_hora:
                            row_errors.append(_('La fecha y hora es obligatoria'))
                        else:
                            # Intentar parsear fecha en formato DD-MM-YYYY HH:MM
                            try:
                                # Convertir formato DD-MM-YYYY HH:MM a datetime
                                parsed_date = datetime.strptime(fecha_hora, '%d-%m-%Y %H:%M')
                                # Hacer timezone aware
                                parsed_date = timezone.make_aware(parsed_date, madrid_tz)
                            except ValueError:
                                row_errors.append(_('Formato de fecha inválido. Use DD-MM-YYYY HH:MM (ej: 15-09-2024 09:00)'))
                                parsed_date = None

                        if not nombre_jugador:
                            row_errors.append(_('El nombre del jugador es obligatorio'))

                        if not apellidos_jugador:
                            row_errors.append(_('Los apellidos del jugador son obligatorios'))

                        # Validar números
                        try:
                            goles_int = int(goles) if goles else 0
                            if goles_int < 0 or goles_int > 20:
                                row_errors.append(_('Goles debe estar entre 0 y 20'))
                        except ValueError:
                            row_errors.append(_('Goles debe ser un número válido'))
                            goles_int = 0

                        try:
                            rojas_int = int(tarjetas_rojas) if tarjetas_rojas else 0
                            if rojas_int < 0 or rojas_int > 1:
                                row_errors.append(_('Tarjetas rojas debe estar entre 0 y 1'))
                        except ValueError:
                            row_errors.append(_('Tarjetas rojas debe ser un número válido'))
                            rojas_int = 0

                        try:
                            amarillas_int = int(tarjetas_amarillas) if tarjetas_amarillas else 0
                            if amarillas_int < 0 or amarillas_int > 2:
                                row_errors.append(_('Tarjetas amarillas debe estar entre 0 y 2'))
                        except ValueError:
                            row_errors.append(_('Tarjetas amarillas debe ser un número válido'))
                            amarillas_int = 0

                        if row_errors:
                            # Prefijo con nombre de archivo para identificar el origen del error
                            prefixed_errors = [f"Archivo '{file_name}' - Fila {row_number}: {error}" for error in row_errors]
                            file_errors.extend(prefixed_errors)
                            continue

                        # Crear objeto de datos para procesamiento
                        stat_data = {
                            'rival_name': rival_name,
                            'match_date': parsed_date,
                            'player_name': nombre_jugador,
                            'player_lastname': apellidos_jugador,
                            'goals': goles_int,
                            'red_cards': rojas_int,
                            'yellow_cards': amarillas_int,
                            'assists': 0,  # No viene en CSV, valor por defecto
                            'minutes_played': 90,  # Valor por defecto
                            'status': 'starter',  # Valor por defecto
                            'attended': True,  # Valor por defecto
                            'source_file': file_name,  # Agregar información del archivo fuente
                        }

                        # Agregar datos formateados para mostrar en la tabla
                        stat_data['display'] = {
                            'rival_name': rival_name,
                            'match_date': parsed_date.strftime('%d/%m/%Y %H:%M') if parsed_date else fecha_hora,
                            'player_full_name': f"{nombre_jugador} {apellidos_jugador}",
                            'goals': str(goles_int),
                            'red_cards': str(rojas_int),
                            'yellow_cards': str(amarillas_int),
                            'source_file': file_name,
                        }

                        stats_to_process.append(stat_data)

                    # Agregar estadísticas de este archivo a la lista total
                    all_stats_to_process.extend(stats_to_process)
                    all_errors.extend(file_errors)
                    total_files_processed += 1

                except Exception as e:
                    all_errors.append(f"Error procesando archivo '{file_name}': {str(e)}")

            if all_errors:
                return JsonResponse({
                    'success': False,
                    'validation_errors': all_errors
                })

            return JsonResponse({
                'success': True,
                'stats': all_stats_to_process,
                'total_stats': len(all_stats_to_process),
                'files_processed': total_files_processed,
                'total_files': len(csv_files)
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': _('Error interno del servidor: %(error)s') % {'error': str(e)}
            })


@method_decorator([login_required], name='dispatch')
class MatchPlayerStatsImportExecuteView(View):
    """Vista para ejecutar la importación final de estadísticas"""

    def post(self, request, *args, **kwargs):
        """Ejecutar la importación de estadísticas"""
        import json
        from datetime import datetime
        from django.utils import timezone
        from django.db import transaction
        from futgoal.season.models import Season
        from futgoal.rivals.models import Rival
        from futgoal.team.models import Team
        from futgoal.players.models import Player

        try:
            # Obtener los datos procesados del POST
            stats_data = json.loads(request.POST.get('stats_data', '[]'))

            if not stats_data:
                return JsonResponse({'success': False, 'error': _('No hay datos para procesar')})

            created_count = 0
            updated_count = 0
            errors = []

            # Obtener temporada activa y equipo local
            active_season = Season.get_active()
            if not active_season:
                return JsonResponse({'success': False, 'error': _('No hay una temporada activa')})

            local_team = Team.objects.first()
            if not local_team:
                return JsonResponse({'success': False, 'error': _('No hay un equipo configurado')})

            with transaction.atomic():
                for stat_data in stats_data:
                    try:
                        # Buscar o crear rival
                        rival, _ = Rival.objects.get_or_create(
                            name=stat_data['rival_name'],
                            defaults={'seasons': [active_season.id] if active_season else []}
                        )

                        # Buscar o crear partido
                        # La fecha viene serializada como string ISO desde JSON
                        try:
                            if isinstance(stat_data['match_date'], str):
                                # Parsear fecha ISO string
                                match_date = parse_datetime(stat_data['match_date'])
                                if not match_date:
                                    # Fallback: intentar con fromisoformat
                                    match_date = datetime.fromisoformat(stat_data['match_date'].replace('Z', '+00:00'))
                            else:
                                # Si viene como datetime objeto, usarlo directamente
                                match_date = stat_data['match_date']

                            # Asegurarse de que sea timezone-aware
                            if match_date and timezone.is_naive(match_date):
                                match_date = timezone.make_aware(match_date)

                        except (ValueError, TypeError) as e:
                            errors.append(f"Error parseando fecha para {stat_data['rival_name']}: {str(e)}")
                            continue

                        match, match_created = Match.objects.get_or_create(
                            home_team=local_team,
                            away_team=rival,
                            match_date=match_date,
                            defaults={
                                'season': active_season,
                                'match_type': 'friendly',
                                'status': 'finished',
                                'venue': '',
                                'is_home': True,
                            }
                        )

                        # Buscar jugador por nombre y apellidos
                        try:
                            player = Player.objects.get(
                                first_name__iexact=stat_data['player_name'],
                                last_name__iexact=stat_data['player_lastname']
                            )
                        except Player.DoesNotExist:
                            # Verificar si son nombres genéricos/placeholder antes de crear
                            player_name = stat_data['player_name'].strip().lower()
                            player_lastname = stat_data['player_lastname'].strip().lower()

                            # Lista de nombres/apellidos genéricos que no deberían crear jugadores
                            generic_names = [
                                'nombre faltante', 'apellidos faltantes', 'apellido faltante',
                                'sin nombre', 'sin apellido', 'sin apellidos',
                                'nombre', 'apellido', 'apellidos',
                                'player', 'jugador', 'desconocido', 'unknown',
                                'n/a', 'na', 'null', 'none', 'vacio', 'vacío',
                                'test', 'prueba', 'ejemplo', 'sample'
                            ]

                            # Verificar si algún campo contiene nombres genéricos
                            is_generic = any(
                                generic in player_name or generic in player_lastname
                                for generic in generic_names
                            )

                            # También verificar si son solo espacios, números o muy cortos
                            is_invalid = (
                                len(player_name.strip()) < 2 or
                                len(player_lastname.strip()) < 2 or
                                player_name.strip().isdigit() or
                                player_lastname.strip().isdigit()
                            )

                            if is_generic or is_invalid:
                                errors.append(f"Jugador {stat_data['player_name']} {stat_data['player_lastname']} no encontrado (nombre genérico o inválido)")
                                continue

                            # Crear jugador automáticamente si tiene nombres reales
                            try:
                                player = Player.objects.create(
                                    first_name=stat_data['player_name'].strip().title(),
                                    last_name=stat_data['player_lastname'].strip().title(),
                                    is_active=True,
                                    # Todos los demás campos son opcionales según el modelo
                                )
                                errors.append(f"✓ Jugador {player.first_name} {player.last_name} creado automáticamente")
                            except Exception as create_error:
                                errors.append(f"Error creando jugador {stat_data['player_name']} {stat_data['player_lastname']}: {str(create_error)}")
                                continue

                        except Player.MultipleObjectsReturned:
                            # Si hay múltiples jugadores con el mismo nombre, tomar el primero activo
                            player = Player.objects.filter(
                                first_name__iexact=stat_data['player_name'],
                                last_name__iexact=stat_data['player_lastname'],
                                is_active=True
                            ).first()
                            if not player:
                                errors.append(f"Múltiples jugadores encontrados para {stat_data['player_name']} {stat_data['player_lastname']}")
                                continue

                        # Crear o actualizar estadísticas
                        stats, stats_created = MatchPlayerStats.objects.update_or_create(
                            match=match,
                            player=player,
                            defaults={
                                'goals': stat_data['goals'],
                                'assists': stat_data.get('assists', 0),
                                'yellow_cards': stat_data['yellow_cards'],
                                'red_cards': stat_data['red_cards'],
                                'minutes_played': stat_data.get('minutes_played', 90),
                                'status': stat_data.get('status', 'starter'),
                                'attended': stat_data.get('attended', True),
                            }
                        )

                        if stats_created:
                            created_count += 1
                        else:
                            updated_count += 1

                    except Exception as e:
                        errors.append(f"Error procesando estadística: {str(e)}")

            # Preparar respuesta
            result = {
                'success': True,
                'created_count': created_count,
                'updated_count': updated_count,
                'total_processed': created_count + updated_count,
            }

            if errors:
                result['warnings'] = errors

            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': _('Error interno del servidor: %(error)s') % {'error': str(e)}
            })
