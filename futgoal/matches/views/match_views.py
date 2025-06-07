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
from django.db.models import Q, Count
from django.views import View
from django.http import JsonResponse, HttpResponse
import json
import csv
import io
from datetime import datetime
from django.utils import timezone

from futgoal.users.decorators import is_global_admin
from futgoal.matches.models import Match
from futgoal.matches.forms import MatchForm, MatchFilterForm, MatchImportForm
from futgoal.season.models import Season
from futgoal.rivals.models import Rival


@method_decorator([login_required, is_global_admin], name='dispatch')
class BaseMatchListView(ListView):
    """Vista base para listar partidos con filtros"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        queryset = Match.objects.select_related('season', 'home_team', 'away_team').prefetch_related('match_notes').annotate(  # pylint: disable=no-member
            notes_count=Count('match_notes')
        ).all()

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

        # Obtener la temporada activa
        active_season = Season.get_active()

        context['page_title'] = _('Partidos')
        context['active_season'] = active_season
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
            {
                'title': _('Importar Partidos'),
                'url': reverse('matches:match_import'),
                'primary': False,
                'icon': '<i class="bi bi-upload"></i>',
                'class': 'btn-success'
            },
        ]

        # Añadir formulario de filtros
        context['filter_form'] = MatchFilterForm(self.request.GET)

        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class UpcomingMatchListView(ListView):
    """Vista para listar próximos partidos"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        from django.db.models import Q

        # Filtrar partidos próximos: futuros o programados
        queryset = Match.objects.filter(  # pylint: disable=no-member
            Q(match_date__gte=timezone.now()) | Q(status='scheduled')
        ).distinct().order_by('match_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la temporada activa
        try:
            active_season = Season.get_active()
        except:
            active_season = None

        context['page_title'] = _('Próximos Partidos')
        context['active_season'] = active_season
        context['active_tab'] = 'upcoming'
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Próximos')}
        ]
        context['actions'] = [
            {
                'title': _('Nuevo Partido'),
                'url': reverse('matches:match_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class PreviousMatchListView(ListView):
    """Vista para listar partidos anteriores"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        from django.db.models import Q

        # Filtrar partidos anteriores: pasados y finalizados/cancelados
        queryset = Match.objects.filter(  # pylint: disable=no-member
            Q(match_date__lt=timezone.now()) &
            ~Q(status='scheduled')  # Excluir los programados que están en próximos
        ).distinct().order_by('-match_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la temporada activa
        try:
            active_season = Season.get_active()
        except:
            active_season = None

        context['page_title'] = _('Partidos Anteriores')
        context['active_season'] = active_season
        context['active_tab'] = 'previous'
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Anteriores')}
        ]
        context['actions'] = [
            {
                'title': _('Nuevo Partido'),
                'url': reverse('matches:match_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
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
        context['delete_message'] = str(_('¿Está seguro de que desea eliminar el partido "{}"?')).format(self.object)
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Partido eliminado correctamente')
        )
        return reverse_lazy('matches:match_list')


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchImportView(View):
    """Vista para importación masiva de partidos"""
    template_name = 'matches/MatchImport.html'

    def get(self, request, *args, **kwargs):
        """Mostrar el formulario de importación"""
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Procesar la importación de partidos"""
        try:
            # Obtener los datos JSON del POST
            matches_data = json.loads(request.body)

            created_matches = []
            errors = []

            for index, match_data in enumerate(matches_data):
                # Crear un formulario para cada partido
                form = MatchImportForm(data=match_data)

                if form.is_valid():
                    try:
                        match = form.save()
                        created_matches.append({
                            'id': match.id,  # pylint: disable=no-member
                            'name': str(match)
                        })
                    except Exception as e:
                        errors.append({
                            'row': index + 1,
                            'message': str(e)
                        })
                else:
                    # Recopilar errores de validación
                    for field, field_errors in form.errors.items():
                        for error in field_errors:
                            errors.append({
                                'row': index + 1,
                                'field': field,
                                'message': error
                            })

            if errors:
                return JsonResponse({
                    'success': False,
                    'errors': errors
                })
            else:
                if created_matches:
                    messages.success(
                        request,
                        _('Se han importado %(count)d partidos correctamente') % {
                            'count': len(created_matches)
                        }
                    )
                return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'errors': [{'message': _('Datos inválidos')}]
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': [{'message': str(e)}]
            })

    def get_context_data(self, **kwargs):
        """Obtener datos del contexto"""
        context = {
            'page_title': _('Importar Partidos'),
            'breadcrumbs': [
                {'title': _('Partidos'), 'url': reverse_lazy('matches:match_list')},
                {'title': _('Importar Partidos')}
            ]
        }
        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchImportCSVTemplateView(View):
    """Vista para descargar la plantilla CSV"""

    def get(self, request, *args, **kwargs):
        """Generar y devolver la plantilla CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="plantilla_partidos.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Rival',
            'Rol (Local/Visitante)',
            'Fecha y Hora (DD/MM/YYYY HH:MM)',
            'Estadio',
            'Tipo de Partido (amistoso, liga, copa, playoff, entrenamiento)',
            'Estado (programado, en_curso, finalizado, cancelado, aplazado)',
            'Goles Local',
            'Goles Visitante'
        ])

        return response


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchProcessCSVView(View):
    """Vista para procesar el archivo CSV de partidos"""

    def post(self, request, *args, **kwargs):
        """Procesar el archivo CSV subido"""
        try:
            if 'csv_file' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': _('No se ha seleccionado ningún archivo')
                })

            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                return JsonResponse({
                    'success': False,
                    'error': _('El archivo debe tener extensión .csv')
                })

            # Leer el archivo CSV
            try:
                decoded_file = csv_file.read().decode('utf-8')
                reader = csv.reader(io.StringIO(decoded_file))
                header = next(reader)  # Saltar la cabecera
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': _('Error al leer el archivo CSV: %(error)s') % {'error': str(e)}
                })

            matches_to_process = []
            errors = []
            for row_num, row in enumerate(reader, start=2):
                if len(row) < 4:
                    errors.append({
                        'row': row_num,
                        'message': _('Fila incompleta. Se requieren al menos 4 columnas.')
                    })
                    continue

                rival_name, role, match_date_str, venue, match_type, status, home_score, away_score = (row + [None]*4)[:8]

                # Validaciones básicas
                if not all([rival_name, role, match_date_str]):
                    errors.append({
                        'row': row_num,
                        'message': _('Faltan campos obligatorios (Equipo rival, Rol, Fecha y hora)')
                    })
                    continue

                is_home = role.strip().lower() == 'local'
                if role.strip().lower() not in ['local', 'visitante']:
                    errors.append({
                        'row': row_num,
                        'message': _('Rol inválido. Use "Local" o "Visitante"')
                    })
                    continue

                try:
                    # Intentar analizar con varios formatos
                    dt = None
                    formats_to_try = ['%d/%m/%Y %H:%M', '%d-%m-%Y %H:%M', '%Y-%m-%d %H:%M']
                    for fmt in formats_to_try:
                        try:
                            dt = datetime.strptime(match_date_str.strip(), fmt)
                            break
                        except ValueError:
                            continue

                    if dt is None:
                        raise ValueError(_('Formato de fecha y hora no válido'))

                    match_date = timezone.make_aware(dt)

                except ValueError as e:
                    errors.append({
                        'row': row_num,
                        'message': _('Formato de fecha y hora inválido. Use DD/MM/YYYY HH:MM')
                    })
                    continue

                matches_to_process.append({
                    'rival': rival_name.strip(),
                    'is_home': is_home,
                    'match_date': match_date.isoformat(),
                    'venue': venue.strip() if venue else '',
                    'match_type': match_type.strip().lower() if match_type else 'friendly',
                    'status': status.strip().lower() if status else 'scheduled',
                    'home_score': int(home_score) if home_score and home_score.strip().isdigit() else None,
                    'away_score': int(away_score) if away_score and away_score.strip().isdigit() else None,
                })

            if errors:
                return JsonResponse({
                    'success': False,
                    'validation_errors': errors
                })

            return JsonResponse({
                'success': True,
                'matches': matches_to_process
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': _('Error interno del servidor: %(error)s') % {'error': str(e)}
            })


@method_decorator([login_required, is_global_admin], name='dispatch')
class InProgressMatchListView(ListView):
    """Vista para listar partidos en curso"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        # Filtrar solo partidos en curso
        queryset = Match.objects.filter(  # pylint: disable=no-member
            status='in_progress'
        ).order_by('-match_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la temporada activa
        try:
            active_season = Season.get_active()
        except:
            active_season = None

        context['page_title'] = _('Partidos en Curso')
        context['active_season'] = active_season
        context['active_tab'] = 'in_progress'
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('En Curso')}
        ]
        context['actions'] = [
            {
                'title': _('Nuevo Partido'),
                'url': reverse('matches:match_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class PostponedMatchListView(ListView):
    """Vista para listar partidos aplazados"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        # Filtrar solo partidos aplazados
        queryset = Match.objects.filter(  # pylint: disable=no-member
            status='postponed'
        ).order_by('-match_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la temporada activa
        try:
            active_season = Season.get_active()
        except:
            active_season = None

        context['page_title'] = _('Partidos Aplazados')
        context['active_season'] = active_season
        context['active_tab'] = 'postponed'
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Aplazados')}
        ]
        context['actions'] = [
            {
                'title': _('Nuevo Partido'),
                'url': reverse('matches:match_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class CancelledMatchListView(ListView):
    """Vista para listar partidos cancelados"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        # Filtrar solo partidos cancelados
        queryset = Match.objects.filter(  # pylint: disable=no-member
            status='cancelled'
        ).order_by('-match_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la temporada activa
        try:
            active_season = Season.get_active()
        except:
            active_season = None

        context['page_title'] = _('Partidos Cancelados')
        context['active_season'] = active_season
        context['active_tab'] = 'cancelled'
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Cancelados')}
        ]
        context['actions'] = [
            {
                'title': _('Nuevo Partido'),
                'url': reverse('matches:match_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class AllMatchListView(ListView):
    """Vista para listar todos los partidos"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        # Mostrar todos los partidos ordenados por fecha descendente
        queryset = Match.objects.all().order_by('-match_date')  # pylint: disable=no-member

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la temporada activa
        try:
            active_season = Season.get_active()
        except:
            active_season = None

        context['page_title'] = _('Todos los Partidos')
        context['active_season'] = active_season
        context['active_tab'] = 'all'
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Todos')}
        ]
        context['actions'] = [
            {
                'title': _('Nuevo Partido'),
                'url': reverse('matches:match_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        return context
