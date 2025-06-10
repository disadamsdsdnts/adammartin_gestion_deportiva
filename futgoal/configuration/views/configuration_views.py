from io import BytesIO
import re
import datetime


from django.views.generic import (
    FormView,
    DetailView,
    UpdateView,
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from futgoal.configuration.forms import ConfigurationUpdateForm
from futgoal.configuration.models import Configuration

from futgoal.matches.models import MatchNote, Match
from futgoal.rivals.models import Rival
from futgoal.players.models import Player
from futgoal.season.models import Season


@method_decorator([login_required], name='dispatch')
class ConfigurationDetailView(DetailView):
    model = Configuration
    template_name = 'configuration/ConfigurationDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Configuración'), 'url': reverse('configuration:configuration_update_list')},
        ]
        context['page_title'] = _('Configuración')
        context['breadcrumbs'] = breadcrumbs
        return context

    def get_object(self):
        return Configuration.objects.first()


@method_decorator([login_required], name='dispatch')
class ConfigurationUpdateView(UpdateView):
    form_class = ConfigurationUpdateForm
    model = Configuration
    template_name = 'configuration/ConfigurationUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Configuración')
        context['breadcrumb_items'] = [_('Configuración')]
        return context

    def get_object(self):
        return Configuration.objects.first()

    def post(self, request, *args, **kwargs):
        # Verificar si es una acción de utilidades del sistema
        action = request.POST.get('action')

        if action == 'delete_all_notes':
            # Borrar todas las notas del sistema
            deleted_count = MatchNote.objects.all().count()
            MatchNote.objects.all().delete()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _('Se han eliminado %(count)d notas correctamente') % {'count': deleted_count}
            )
            return HttpResponseRedirect(reverse('configuration:configuration_update'))

        elif action == 'delete_all_rivals':
            # Borrar todos los rivales del sistema
            deleted_count = Rival.objects.all().count()
            Rival.objects.all().delete()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _('Se han eliminado %(count)d rivales correctamente') % {'count': deleted_count}
            )
            return HttpResponseRedirect(reverse('configuration:configuration_update'))

        elif action == 'delete_all_matches':
            # Borrar todos los partidos del sistema
            deleted_count = Match.objects.all().count()
            Match.objects.all().delete()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _('Se han eliminado %(count)d partidos correctamente') % {'count': deleted_count}
            )
            return HttpResponseRedirect(reverse('configuration:configuration_update'))

        elif action == 'delete_all_players':
            # Borrar todos los jugadores del sistema
            deleted_count = Player.objects.all().count()
            Player.objects.all().delete()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _('Se han eliminado %(count)d jugadores correctamente') % {'count': deleted_count}
            )
            return HttpResponseRedirect(reverse('configuration:configuration_update'))

        elif action == 'delete_all_seasons':
            # Borrar todas las temporadas del sistema
            deleted_count = Season.objects.all().count()
            Season.objects.all().delete()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _('Se han eliminado %(count)d temporadas correctamente') % {'count': deleted_count}
            )
            return HttpResponseRedirect(reverse('configuration:configuration_update'))

        elif action == 'delete_all_data':
            # Borrar TODOS los datos del sistema
            notes_count = MatchNote.objects.all().count()
            rivals_count = Rival.objects.all().count()
            matches_count = Match.objects.all().count()
            players_count = Player.objects.all().count()
            seasons_count = Season.objects.all().count()

            # Eliminar en orden para evitar problemas de dependencias
            MatchNote.objects.all().delete()
            Match.objects.all().delete()  # Los partidos antes que rivales y temporadas
            Player.objects.all().delete()
            Rival.objects.all().delete()
            Season.objects.all().delete()

            total_count = notes_count + rivals_count + matches_count + players_count + seasons_count

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _('Se han eliminado todos los datos: %(notes)d notas, %(rivals)d rivales, %(matches)d partidos, %(players)d jugadores y %(seasons)d temporadas (Total: %(total)d registros)') % {
                    'notes': notes_count,
                    'rivals': rivals_count,
                    'matches': matches_count,
                    'players': players_count,
                    'seasons': seasons_count,
                    'total': total_count
                }
            )
            return HttpResponseRedirect(reverse('configuration:configuration_update'))

        # Si no es una acción de utilidades, procesar normalmente el formulario
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Configuración actualizada correctamente')
        )
        return reverse_lazy('configuration:configuration_update')
