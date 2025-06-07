from django.contrib import messages
from django.urls import reverse, reverse_lazy
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
from futgoal.season.models import Season
from .models import Rival
from .forms import RivalForm, ImportRivalsForm


@method_decorator([login_required, is_global_admin], name='dispatch')
class RivalListView(ListView):
    """Vista para listar equipos rivales"""
    template_name = 'rivals/RivalsList.html'
    model = Rival
    context_object_name = 'rivals'
    paginate_by = 20

    def get_queryset(self):
        # Por defecto mostrar solo rivales de la temporada activa, mostrar todos solo si se solicita
        show_all = self.request.GET.get('show_all', '')

        if show_all:
            # Mostrar todos los rivales cuando se solicite explícitamente
            queryset = Rival.objects.all()
        else:
            # Por defecto, filtrar por temporada activa
            active_season = Season.get_active()
            if active_season:
                queryset = Rival.objects.filter(seasons=active_season)
            else:
                # Si no hay temporada activa, mostrar todos
                queryset = Rival.objects.all()

        # Filtro de búsqueda
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(coach_name__icontains=search) |
                Q(city__icontains=search) |
                Q(field_name__icontains=search)
            )

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_season = Season.get_active()
        show_all = self.request.GET.get('show_all', '')

        context['page_title'] = _('Equipos Rivales')
        context['breadcrumbs'] = [
            {'title': _('Equipos Rivales'), 'url': reverse('rivals:rival_list')},
        ]
        context['action_button'] = f'<a href="{reverse_lazy("rivals:rival_create")}" class="inline-flex items-center justify-center w-1/2 px-3 py-2 text-sm font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 sm:w-auto dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"><svg class="w-5 h-5 mr-2 -ml-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path></svg>{_("Nuevo Rival")}</a>'

        # Información adicional de contexto
        context['active_season'] = active_season
        context['show_all'] = show_all

        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class RivalDetailView(DetailView):
    """Vista para ver detalle de un equipo rival"""
    template_name = 'rivals/RivalDetail.html'
    model = Rival
    context_object_name = 'rival'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = f"{_('Rival')}: {self.object.name}"
        context['breadcrumbs'] = [
            {'title': _('Equipos Rivales'), 'url': reverse('rivals:rival_list')},
            {'title': self.object.name}
        ]
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('rivals:rival_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
            {
                'title': _('Eliminar'),
                'url': reverse('rivals:rival_delete', kwargs={'pk': self.object.pk}),
                'danger': True,
                'icon': '<i class="bi bi-trash"></i>'
            },
        ]
        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class RivalCreateView(CreateView):
    """Vista para crear un nuevo equipo rival"""
    template_name = 'rivals/RivalCreate.html'
    model = Rival
    form_class = RivalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = _('Nuevo Equipo Rival')
        context['breadcrumbs'] = [
            {'title': _('Equipos Rivales'), 'url': reverse('rivals:rival_list')},
            {'title': _('Nuevo'), 'url': reverse('rivals:rival_create')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Equipo rival creado correctamente')
        )
        return reverse_lazy('rivals:rival_detail', kwargs={'pk': self.object.pk})


@method_decorator([login_required, is_global_admin], name='dispatch')
class RivalUpdateView(UpdateView):
    """Vista para editar un equipo rival"""
    template_name = 'rivals/RivalUpdate.html'
    model = Rival
    form_class = RivalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = _('Editar Equipo Rival')
        context['breadcrumbs'] = [
            {'title': _('Equipos Rivales'), 'url': reverse('rivals:rival_list')},
            {'title': self.object.name, 'url': reverse('rivals:rival_detail', kwargs={'pk': self.object.pk})},
            {'title': _('Editar')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Equipo rival modificado correctamente')
        )
        return reverse_lazy('rivals:rival_detail', kwargs={'pk': self.object.pk})


@method_decorator([login_required, is_global_admin], name='dispatch')
class RivalDeleteView(DeleteView):
    """Vista para eliminar un equipo rival"""
    model = Rival
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = _("Eliminar Equipo Rival")
        context['breadcrumbs'] = [
            {'title': _('Equipos Rivales'), 'url': reverse('rivals:rival_list')},
            {'title': self.object.name, 'url': reverse('rivals:rival_detail', kwargs={'pk': self.object.pk})},
            {'title': _('Eliminar')},
        ]
        context['delete_message'] = _('¿Está seguro de que desea eliminar el equipo rival "{}"?').format(self.object.name)
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Equipo rival eliminado correctamente')
        )
        return reverse_lazy('rivals:rival_list')
