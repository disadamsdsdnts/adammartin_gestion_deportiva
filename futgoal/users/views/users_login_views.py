# -*- encoding: utf-8 -*-
"""Users views."""
import hashlib

from django.contrib.auth import login, authenticate, logout
from datetime import date
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils import timezone

from django.contrib import messages

from django.utils import translation

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    RedirectView
)

from django.contrib.auth.decorators import login_required

from futgoal.users.decorators import (
    is_global_admin,
)

from futgoal.users.forms import LoginForm, RememberForm, PasswordForm, LoginCodeForm
from futgoal.users.models import User
from futgoal.users.forms.auth_forms import CustomAuthenticationForm

decorators = [
    csrf_protect,
    never_cache,
]


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'users/dashboard/Dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el equipo tiene datos básicos configurados
        from futgoal.team.models import Team

        if not Team.is_configured():
            messages.add_message(
                request,
                messages.INFO,
                _('¡Bienvenido! Por favor, configura los datos básicos de tu equipo para comenzar.')
            )
            return HttpResponseRedirect(reverse('team:update') + '?setup=initial')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
        ]
        context['page_title'] = _('Dashboard')
        context['breadcrumbs'] = breadcrumbs
        context['actions'] = []

        # Obtener próximos partidos (máximo 5)
        from futgoal.matches.models import Match
        upcoming_matches = Match.objects.filter(
            status='scheduled',
            match_date__gt=timezone.now()
        ).select_related('away_team', 'season').order_by('match_date')[:5]

        context['upcoming_matches'] = upcoming_matches

        # Obtener próximos cumpleaños (máximo 5)
        from futgoal.players.models import Player
        from datetime import datetime, timedelta

        today = timezone.now().date()
        current_year = today.year

        # Obtener jugadores activos con fecha de nacimiento
        players = Player.objects.filter(
            is_active=True,
            birth_date__isnull=False
        ).values('id', 'first_name', 'last_name', 'sport_name', 'birth_date', 'photo')

        # Calcular próximos cumpleaños
        upcoming_birthdays = []
        for player in players:
            birth_date = player['birth_date']

            # Crear fecha de cumpleaños para este año
            try:
                birthday_this_year = birth_date.replace(year=current_year)
            except ValueError:
                # Manejar 29 de febrero en años no bisiestos
                birthday_this_year = birth_date.replace(year=current_year, day=28)

            # Si ya pasó este año, usar el próximo año
            if birthday_this_year < today:
                try:
                    birthday_this_year = birth_date.replace(year=current_year + 1)
                except ValueError:
                    birthday_this_year = birth_date.replace(year=current_year + 1, day=28)

            # Calcular días hasta el cumpleaños
            days_until = (birthday_this_year - today).days

            # Calcular edad que cumplirá
            age = birthday_this_year.year - birth_date.year

            upcoming_birthdays.append({
                'player': player,
                'birthday_date': birthday_this_year,
                'days_until': days_until,
                'age': age
            })

        # Ordenar por días hasta cumpleaños y tomar los primeros 5
        upcoming_birthdays.sort(key=lambda x: x['days_until'])
        context['upcoming_birthdays'] = upcoming_birthdays[:5]

        # Obtener estadísticas de la temporada actual
        from futgoal.season.models import Season
        from django.db.models import Q, Count

        try:
            # Obtener la temporada actual
            current_season = Season.objects.get(is_active=True)

            # Obtener todos los partidos de la temporada actual
            season_matches = Match.objects.filter(season=current_season)

            # Contar estadísticas
            total_matches = season_matches.count()

            # Para contar wins/draws/losses necesitamos evaluar cada partido finalizado
            wins = 0
            draws = 0
            losses = 0

            finished_matches = season_matches.filter(status='finished')
            for match in finished_matches:
                result_status = match.match_result_status
                if result_status == 'victory':
                    wins += 1
                elif result_status == 'draw':
                    draws += 1
                elif result_status == 'defeat':
                    losses += 1

            pending = season_matches.filter(status='scheduled').count()

            # Calcular porcentajes
            if total_matches > 0:
                win_percentage = round((wins / total_matches) * 100, 1)
                draw_percentage = round((draws / total_matches) * 100, 1)
                loss_percentage = round((losses / total_matches) * 100, 1)
                pending_percentage = round((pending / total_matches) * 100, 1)
            else:
                win_percentage = draw_percentage = loss_percentage = pending_percentage = 0

            # Crear diccionario con estadísticas
            season_stats = {
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'pending': pending,
                'total_matches': total_matches,
                'win_percentage': win_percentage,
                'draw_percentage': draw_percentage,
                'loss_percentage': loss_percentage,
                'pending_percentage': pending_percentage,
            }

            context['season_stats'] = season_stats

        except Season.DoesNotExist:
            # Si no hay temporada actual, no mostrar estadísticas
            context['season_stats'] = None

        return context


class Error404View(TemplateView):
    template_name = 'users/error404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(FormView):
    template_name = 'users/login/UserLogin.html'
    form_class = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return super().dispatch(
                request, *args, **kwargs
            )

    def form_valid(self, form):
        login(self.request, form.get_user())
        form.get_user().add_action(_("User logged in"))
        return HttpResponseRedirect(
            self.request.GET.get('next', reverse('dashboard'))
        )


class LoginWithUUID(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        # obtento el parámetro uuid de la url
        uuid = kwargs.get('uuid')
        # obtengo el usuario con ese uuid
        user = get_object_or_404(User, uuid=uuid)
        if user.is_active:
            # autentico al usuario
            login(request, user)
            # redirijo a la página de dashboard
            request.session['sales_boss'] = True
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return super().dispatch(
                request, *args, **kwargs
            )

class RememberPassword(FormView):
    template_name = 'users/login/UsersRememberPassword.html'
    form_class = RememberForm
    success_url = reverse_lazy('auth:remember_password_email_sended')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            msg = _('No existe usuario con ese email')
            form._errors['email'] = [msg]
            return super(RememberPassword, self).form_invalid(form)

        user.send_email_remember_password()
        return super(RememberPassword, self).form_valid(form)


class TypeYourPassword(FormView):
    form_class = PasswordForm
    template_name = 'users/login/UsersTypePassword.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        return {
            'remember_key': self.kwargs.get('remember_key')
        }

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        remember_key = kwargs['remember_key']
        if User.objects.filter(remember_key=remember_key).count() == 0:
            self.user = None
            messages.add_message(
                self.request, messages.ERROR,
                _('Enlace caducado, vuelva a solicitar recordar contraseña'))

            return HttpResponseRedirect(reverse_lazy('auth:remember_password_form'))
        else:
            self.user = User.objects.get(remember_key=remember_key)
        return super(TypeYourPassword, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        self.user.set_password(form.data['password2'])
        self.user.save()
        # self.user.add_action(_('Reset password'))
        return super(TypeYourPassword, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS,
            _('Password cambiado correctamente'))
        return reverse_lazy('auth:login')


class RememberEmailSended(TemplateView):
    template_name = 'users/login/UsersPasswordResetOk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@ login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth:login'))
