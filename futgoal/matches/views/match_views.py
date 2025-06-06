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

from futgoal.users.decorators import is_global_admin
from futgoal.matches.models import Match
from futgoal.matches.forms import MatchForm, MatchFilterForm, MatchImportForm
from futgoal.season.models import Season
from futgoal.rivals.models import Rival


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchListView(ListView):
    """Vista para listar partidos"""
    template_name = 'matches/MatchesList.html'
    model = Match
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        queryset = Match.objects.select_related('season', 'home_team', 'away_team').prefetch_related('match_notes').annotate(
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
                            'id': match.id,
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
                                'message': str(error)
                            })

            # Preparar respuesta
            response_data = {
                'success': len(errors) == 0,
                'created_count': len(created_matches),
                'errors': errors,
                'created_matches': created_matches
            }

            if response_data['success']:
                messages.success(
                    request,
                    _('Se han importado %(count)d partidos correctamente') % {
                        'count': len(created_matches)
                    }
                )

            return JsonResponse(response_data)

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
    """Vista para descargar plantilla CSV de importación"""

    def get(self, request, *args, **kwargs):
        """Generar y descargar plantilla CSV"""
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="plantilla_partidos.csv"'

        # Añadir BOM para Excel
        response.write('\ufeff')

        writer = csv.writer(response)

        # Escribir headers
        writer.writerow([
            'Equipo rival',
            'Rol (Local/Visitante)',
            'Fecha y hora (DD/MM/YYYY HH:MM)',
            'Tipo de partido',
            'Lugar del partido'
        ])

        # Escribir algunas filas de ejemplo
        writer.writerow([
            'Barcelona FC',
            'Local',
            '25/12/2024 19:00',
            'Amistoso',
            'Camp Nou'
        ])
        writer.writerow([
            'Real Madrid',
            'Visitante',
            '15/01/2025 21:30',
            'Liga',
            'Santiago Bernabéu'
        ])
        writer.writerow([
            'Valencia CF',
            'Local',
            '20/02/2025 18:00',
            'Copa',
            'Mestalla'
        ])

        return response


@method_decorator([login_required, is_global_admin], name='dispatch')
class MatchProcessCSVView(View):
    """Vista para procesar archivo CSV subido"""

    def post(self, request, *args, **kwargs):
        """Procesar archivo CSV y devolver datos JSON"""
        try:
            if 'csv_file' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': _('No se ha seleccionado ningún archivo')
                })

            csv_file = request.FILES['csv_file']

            # Validar que es un archivo CSV
            if not csv_file.name.endswith('.csv'):
                return JsonResponse({
                    'success': False,
                    'error': _('El archivo debe tener extensión .csv')
                })

            # Leer el archivo CSV
            try:
                # Intentar detectar el encoding
                file_content = csv_file.read()
                csv_file.seek(0)

                # Intentar UTF-8 primero, luego latin-1
                try:
                    decoded_content = file_content.decode('utf-8-sig')
                except UnicodeDecodeError:
                    try:
                        decoded_content = file_content.decode('latin-1')
                    except UnicodeDecodeError:
                        decoded_content = file_content.decode('cp1252')

                # Crear un objeto StringIO para csv.reader
                csv_content = io.StringIO(decoded_content)
                reader = csv.reader(csv_content, delimiter=',')

                matches_data = []
                errors = []

                # Saltar la primera fila (headers)
                next(reader, None)

                for row_num, row in enumerate(reader, start=2):
                    if len(row) < 4:  # Verificar que tenga al menos 4 columnas obligatorias
                        errors.append({
                            'row': row_num,
                            'message': _('Fila incompleta. Se requieren al menos 4 columnas.')
                        })
                        continue

                    # Obtener campos obligatorios
                    rival_name, role, match_date_str, match_type = [cell.strip() for cell in row[:4]]

                    # Obtener campo opcional venue (lugar del partido)
                    venue = row[4].strip() if len(row) > 4 else ''

                    # Validar que todos los campos requeridos tienen contenido
                    if not all([rival_name, role, match_date_str]):
                        errors.append({
                            'row': row_num,
                            'message': _('Faltan campos obligatorios (Equipo rival, Rol, Fecha y hora)')
                        })
                        continue

                    # El nombre del rival se usará directamente (se creará automáticamente si no existe)

                    # Validar y convertir rol
                    role_value = None
                    role_lower = role.lower()
                    if role_lower in ['local', 'home', 'casa']:
                        role_value = '1'  # True para local
                    elif role_lower in ['visitante', 'away', 'fuera']:
                        role_value = '0'  # False para visitante
                    else:
                        errors.append({
                            'row': row_num,
                            'message': _('Rol inválido. Use "Local" o "Visitante"')
                        })
                        continue

                    # Validar y convertir fecha y hora
                    match_date = None
                    try:
                        # Intentar diferentes formatos de fecha y hora
                        for datetime_format in [
                            '%d/%m/%Y %H:%M',
                            '%Y-%m-%d %H:%M',
                            '%d-%m-%Y %H:%M',
                            '%m/%d/%Y %H:%M',
                            '%d/%m/%Y %H:%M:%S',
                            '%Y-%m-%d %H:%M:%S'
                        ]:
                            try:
                                match_date = datetime.strptime(match_date_str, datetime_format)
                                break
                            except ValueError:
                                continue

                        if match_date is None:
                            raise ValueError(_('Formato de fecha y hora no válido'))

                    except ValueError as e:
                        errors.append({
                            'row': row_num,
                            'message': _('Formato de fecha y hora inválido. Use DD/MM/YYYY HH:MM')
                        })
                        continue

                    # Convertir fecha al formato ISO para JavaScript
                    match_date_iso = match_date.strftime('%Y-%m-%dT%H:%M')

                    # Validar tipo de partido (opcional, por defecto 'friendly')
                    valid_match_types = dict(Match.MATCH_TYPE_CHOICES)
                    match_type_key = match_type.lower() if match_type else 'friendly'

                    # Mapear nombres en español a códigos
                    type_mapping = {
                        'amistoso': 'friendly',
                        'liga': 'league',
                        'copa': 'cup',
                        'playoff': 'playoff',
                        'entrenamiento': 'training'
                    }

                    if match_type_key in type_mapping:
                        match_type_key = type_mapping[match_type_key]
                    elif match_type_key not in valid_match_types:
                        match_type_key = 'friendly'  # Por defecto

                    matches_data.append({
                        'rival_name': rival_name,
                        'role': role_value,
                        'match_date': match_date_iso,
                        'match_type': match_type_key,
                        'venue': venue,
                        'row': row_num
                    })

                return JsonResponse({
                    'success': True,
                    'matches_data': matches_data,
                    'total_rows': len(matches_data),
                    'errors': errors
                })

            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': _('Error al procesar el archivo CSV: %(error)s') % {'error': str(e)}
                })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': _('Error interno del servidor: %(error)s') % {'error': str(e)}
            })
