from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.forms import formset_factory
from django.shortcuts import render, redirect
import json
import csv
import io
from datetime import datetime

from ..models.player import Player
from ..forms.player_forms import PlayerForm, PlayerImportForm

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
        context['action_button'] = f'''
            <a href="{reverse_lazy("players:player_create")}" class="inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 sm:w-auto dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                <svg class="w-5 h-5 mr-2 -ml-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path>
                </svg>
                {_("Añadir jugador")}
            </a>
            <a href="{reverse_lazy("players:player_import")}" class="inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-center text-white rounded-lg bg-green-600 hover:bg-green-700 focus:ring-4 focus:ring-green-300 sm:w-auto dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800 ml-2">
                <svg class="w-5 h-5 mr-2 -ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                </svg>
                {_("Importar jugadores")}
            </a>
        '''
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

class PlayerImportView(LoginRequiredMixin, View):
    """Vista para importación masiva de jugadores"""
    template_name = 'players/PlayerImport.html'

    def get(self, request, *args, **kwargs):
        """Mostrar el formulario de importación"""
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Procesar la importación de jugadores"""
        try:
            # Obtener los datos JSON del POST
            players_data = json.loads(request.body)

            created_players = []
            errors = []

            for index, player_data in enumerate(players_data):
                # Crear un formulario para cada jugador
                form = PlayerImportForm(data=player_data)

                if form.is_valid():
                    try:
                        player = form.save()
                        created_players.append({
                            'id': player.id,
                            'name': player.full_name
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
                'created_count': len(created_players),
                'errors': errors,
                'created_players': created_players
            }

            if response_data['success']:
                messages.success(
                    request,
                    _('Se han importado %(count)d jugadores correctamente') % {
                        'count': len(created_players)
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
            'page_title': _('Importar Jugadores'),
            'breadcrumbs': [
                {'title': _('Jugadores'), 'url': reverse_lazy('players:player_list')},
                {'title': _('Importar Jugadores')}
            ]
        }
        return context

class PlayerImportCSVTemplateView(LoginRequiredMixin, View):
    """Vista para descargar plantilla CSV de importación"""

    def get(self, request, *args, **kwargs):
        """Generar y descargar plantilla CSV"""
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="plantilla_jugadores.csv"'

        # Añadir BOM para Excel
        response.write('\ufeff')

        writer = csv.writer(response)

        # Escribir headers
        writer.writerow([
            'Nombre',
            'Apellidos',
            'Fecha de nacimiento (DD/MM/YYYY)',
            'Documento de identidad'
        ])

        # Escribir algunas filas de ejemplo
        writer.writerow([
            'Juan',
            'Pérez García',
            '15/03/1995',
            '12345678A'
        ])
        writer.writerow([
            'María',
            'González López',
            '22/07/1998',
            '87654321B'
        ])
        writer.writerow([
            'Carlos',
            'Martín Ruiz',
            '10/12/1992',
            '11223344C'
        ])

        return response


class PlayerProcessCSVView(LoginRequiredMixin, View):
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

                players_data = []
                errors = []

                # Saltar la primera fila (headers)
                next(reader, None)

                for row_num, row in enumerate(reader, start=2):  # Empezar desde fila 2
                    if len(row) < 4:
                        if any(cell.strip() for cell in row):  # Si la fila no está completamente vacía
                            errors.append({
                                'row': row_num,
                                'message': _('La fila debe tener exactamente 4 columnas: Nombre, Apellidos, Fecha de nacimiento, Documento de identidad')
                            })
                        continue

                    first_name = row[0].strip()
                    last_name = row[1].strip()
                    birth_date_str = row[2].strip()
                    identity_document = row[3].strip()

                    # Validar que todos los campos requeridos están presentes
                    if not all([first_name, last_name, birth_date_str, identity_document]):
                        errors.append({
                            'row': row_num,
                            'message': _('Todos los campos son obligatorios')
                        })
                        continue

                    # Procesar fecha de nacimiento
                    birth_date = None
                    try:
                        # Intentar diferentes formatos de fecha
                        for date_format in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']:
                            try:
                                birth_date = datetime.strptime(birth_date_str, date_format).date()
                                break
                            except ValueError:
                                continue

                        if birth_date is None:
                            raise ValueError(_('Formato de fecha no válido'))

                    except ValueError as e:
                        errors.append({
                            'row': row_num,
                            'message': _('Formato de fecha inválido. Use DD/MM/YYYY')
                        })
                        continue

                    # Convertir fecha al formato ISO para JavaScript
                    birth_date_iso = birth_date.strftime('%Y-%m-%d')

                    players_data.append({
                        'first_name': first_name,
                        'last_name': last_name,
                        'birth_date': birth_date_iso,
                        'identity_document': identity_document,
                        'row': row_num
                    })

                return JsonResponse({
                    'success': True,
                    'players_data': players_data,
                    'total_rows': len(players_data),
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
