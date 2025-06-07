from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, FormView
from datetime import datetime, date

from futgoal.team.models import Team
from futgoal.team.forms import TeamUpdateForm
from futgoal.season.models import Season
from futgoal.season.forms import SeasonForm


def needs_onboarding():
    """
    Función que determina si se necesita mostrar el onboarding.
    Retorna True si:
    - No hay un equipo configurado (sin nombre)
    - No hay temporadas creadas
    """
    # Verificar equipo
    if not Team.is_configured():
        return True

    # Verificar temporadas
    if not Season.objects.exists():
        return True

    return False


@method_decorator(login_required, name='dispatch')
class OnboardingWelcomeView(TemplateView):
    """Primera pantalla: Bienvenida con explicación de los pasos"""
    template_name = 'users/onboarding/OnboardingWelcome.html'

    def dispatch(self, request, *args, **kwargs):
        # Si no necesita onboarding, redirigir al dashboard
        if not needs_onboarding():
            return HttpResponseRedirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('¡Bienvenido a FutGoal!')
        return context


@method_decorator(login_required, name='dispatch')
class OnboardingTeamView(FormView):
    """Segunda pantalla: Configurar datos del equipo"""
    template_name = 'users/onboarding/OnboardingTeam.html'
    form_class = TeamUpdateForm

    def dispatch(self, request, *args, **kwargs):
        # Si no necesita onboarding, redirigir al dashboard
        if not needs_onboarding():
            return HttpResponseRedirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return Team.get_or_create_team()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        kwargs['is_initial_setup'] = True
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Configurar tu equipo')
        context['current_step'] = 2
        context['total_steps'] = 4
        context['team'] = self.get_object()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            _('¡Excelente! Los datos de tu equipo han sido configurados.')
        )
        return HttpResponseRedirect(reverse('onboarding_season'))


@method_decorator(login_required, name='dispatch')
class OnboardingSeasonView(FormView):
    """Tercera pantalla: Crear temporada inicial"""
    template_name = 'users/onboarding/OnboardingSeason.html'
    form_class = SeasonForm

    def dispatch(self, request, *args, **kwargs):
        # Si no necesita onboarding, redirigir al dashboard
        if not needs_onboarding():
            return HttpResponseRedirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Proporcionar valores iniciales para el formulario"""
        initial = super().get_initial()
        current_year = datetime.now().year

        # Sugerir nombre de temporada con año actual
        initial['name'] = f'Temporada {current_year}-{current_year + 1}'

        # Sugerir fechas por defecto (agosto a junio)
        initial['start_date'] = date(current_year, 8, 1)
        initial['end_date'] = date(current_year + 1, 6, 30)

        # Marcar como activa por defecto
        initial['is_active'] = True

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Crear temporada inicial')
        context['current_step'] = 3
        context['total_steps'] = 4
        context['team'] = Team.objects.first()
        return context

    def form_valid(self, form):
        season = form.save()
        messages.success(
            self.request,
            _('¡Perfecto! Tu temporada inicial ha sido creada y activada.')
        )
        return HttpResponseRedirect(reverse('onboarding_complete'))


@method_decorator(login_required, name='dispatch')
class OnboardingCompleteView(TemplateView):
    """Cuarta pantalla: Onboarding completado"""
    template_name = 'users/onboarding/OnboardingComplete.html'

    def dispatch(self, request, *args, **kwargs):
        # Si no necesita onboarding, redirigir al dashboard
        if not needs_onboarding():
            return HttpResponseRedirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('¡Todo listo!')
        context['current_step'] = 4
        context['total_steps'] = 4
        context['team'] = Team.objects.first()
        context['active_season'] = Season.get_active()
        return context
