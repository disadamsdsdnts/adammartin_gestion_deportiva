from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from futgoal.matches.models import Match, MatchNote
from futgoal.matches.forms.match_note_forms import MatchNoteForm


@method_decorator([login_required], name='dispatch')
class MatchNoteListView(ListView):
    """Vista para listar todas las notas de partido"""
    template_name = 'matches/MatchNotesList.html'
    model = MatchNote
    context_object_name = 'notes'
    paginate_by = 20

    def get_queryset(self):
        queryset = MatchNote.objects.select_related('match', 'match__home_team', 'match__away_team', 'match__season')

        # Agregar funcionalidad de búsqueda
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(match__away_team__name__icontains=search_query) |
                Q(match__home_team__name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Notas de Partidos')
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Notas'), 'url': reverse('matches:match_note_list')},
        ]
        context['actions'] = [
            {
                'title': _('Volver a Partidos'),
                'url': reverse('matches:match_list'),
                'primary': False,
                'icon': '<i class="bi bi-arrow-left"></i>'
            },
        ]

        # Agregar funcionalidad de búsqueda
        context['search_placeholder'] = _('Buscar notas por título, contenido o equipo...')
        context['search_query'] = self.request.GET.get('search', '')

        return context


@method_decorator([login_required], name='dispatch')
class MatchNoteDetailView(DetailView):
    """Vista para mostrar el detalle de una nota de partido"""
    template_name = 'matches/MatchNoteDetail.html'
    model = MatchNote
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{_('Nota')}: {self.object.title}"
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': _('Notas'), 'url': reverse('matches:match_note_list')},
            {'title': self.object.title}
        ]
        return context


@method_decorator([login_required], name='dispatch')
class MatchNoteCreateView(CreateView):
    """Vista para crear una nueva nota de partido"""
    template_name = 'matches/MatchNoteCreate.html'
    model = MatchNote
    form_class = MatchNoteForm

    def get_match(self):
        """Obtiene el partido desde la URL"""
        match_id = self.kwargs.get('match_id')
        return get_object_or_404(Match, pk=match_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['match'] = self.get_match()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.get_match()
        context['match'] = match
        context['page_title'] = _('Nueva Nota de Partido')
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': str(match), 'url': reverse('matches:match_detail', kwargs={'pk': match.pk})},
            {'title': _('Nueva Nota')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Nota creada correctamente')
        )
        return reverse_lazy('matches:match_detail', kwargs={'pk': self.get_match().pk})


@method_decorator([login_required], name='dispatch')
class MatchNoteUpdateView(UpdateView):
    """Vista para editar una nota de partido"""
    template_name = 'matches/MatchNoteUpdate.html'
    model = MatchNote
    form_class = MatchNoteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['match'] = self.object.match
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Editar Nota')
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': str(self.object.match), 'url': reverse('matches:match_detail', kwargs={'pk': self.object.match.pk})},
            {'title': _('Editar Nota')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Nota modificada correctamente')
        )
        return reverse_lazy('matches:match_detail', kwargs={'pk': self.object.match.pk})


@method_decorator([login_required], name='dispatch')
class MatchNoteDeleteView(DeleteView):
    """Vista para eliminar una nota de partido"""
    model = MatchNote
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Eliminar Nota")
        context['breadcrumbs'] = [
            {'title': _('Partidos'), 'url': reverse('matches:match_list')},
            {'title': str(self.object.match), 'url': reverse('matches:match_detail', kwargs={'pk': self.object.match.pk})},
            {'title': _('Eliminar Nota')},
        ]
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Nota eliminada correctamente')
        )
        return reverse_lazy('matches:match_detail', kwargs={'pk': self.object.match.pk})


@login_required
def delete_match_note_ajax(request, pk):
    """Vista AJAX para eliminar una nota de partido"""
    try:
        note = get_object_or_404(MatchNote, pk=pk)
        match_pk = note.match.pk
        note.delete()
        return JsonResponse({
            'status': 'success',
            'message': _('Nota eliminada correctamente'),
            'redirect_url': reverse('matches:match_detail', kwargs={'pk': match_pk})
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': _('Error al eliminar la nota')
        })
