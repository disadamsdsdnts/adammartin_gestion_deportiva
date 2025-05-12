import requests
from io import BytesIO
import re
from django.contrib.auth.models import Group

# Django
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView
)
from django.http import HttpResponse
from django.utils import translation

from futgoal.users.models import User

from futgoal.users.forms.user_form import(
    UserCreateForm,
    UserUpdateForm,
)

from futgoal.users.decorators import (
    is_global_admin,
)


@method_decorator([is_global_admin], name='dispatch')
class GaUserListView(TemplateView):
    template_name = 'users/GaUserList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
        ]
        context['page_title'] = _('Usuarios')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('users:ga_user_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']

        sales_teams = []
        sale_teams =  Group.objects.exclude(name__startswith='Closers').exclude(name__startswith='Lí').exclude(name__startswith='So').exclude(name__startswith='Ch').exclude(name__startswith='Se').exclude(name__startswith='Fa').order_by('name')
        for st in sale_teams:
            sales_teams.append(
                {
                    'id': st.id,
                    'name': st.name,
                    'users': User.objects.filter(sale_team=st, is_active=True).order_by('first_name')
                })
        context['sales_teams'] = sales_teams

        other_teams = []
        support_teams =  Group.objects.filter(name__startswith='So').order_by('name')
        for st in support_teams:
            other_teams.append(
                {
                    'id': st.id,
                    'name': st.name,
                    'users': User.objects.filter(groups__in=support_teams, is_active=True).order_by('first_name')
                })
        context['other_teams'] = other_teams

        return context



@method_decorator([is_global_admin], name='dispatch')
class GaUserDetailView(DetailView):
    template_name = 'users/GaUserDetail.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
            {'title': self.object.full_name}
        ]
        context['page_title'] = f"{_('Usuario')} : {self.object.full_name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('users:ga_user_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context


@method_decorator([is_global_admin], name='dispatch')
class GaUserCreateView(CreateView):
    template_name = 'users/GaUserCreate.html'
    model = User
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
            {'title': _('Nuevo usuario'), 'url': reverse(
                'users:ga_user_create')},
        ]
        context['page_title'] = _('Nuevo Usuario')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario creado correctamente')
        )
        return reverse_lazy(
            'users:ga_user_list'
        )


@method_decorator((is_global_admin), name='dispatch')
class GaUserUpdateView(UpdateView):
    template_name = 'users/GaUserUpdate.html'
    model = User
    form_class = UserUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
            {'title': _('Editar usuario')},
        ]
        context['page_title'] = _('Editar Usuario')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario modificado correctamente')
        )

        return reverse_lazy(
            'users:ga_user_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator((is_global_admin), name='dispatch')
class GaUserDeleteView(DeleteView):
    model = User
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Usuario")
        context['breadcrums'] = breadcrums

        return context

    def get_confirm_text_message(self):
        return _('¿Seguro que desea <span class="kt-font-bold">eliminar el Usuario %s</span>? Se borrarán todos los datos asociados al mismo.') % self.object.email

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario eliminado correctamente')
        )

        return reverse_lazy(
            'users:ga_user_list'
        )
