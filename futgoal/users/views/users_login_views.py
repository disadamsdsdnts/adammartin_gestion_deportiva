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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
        ]
        context['page_title'] = f"{_('Dashboard')}"
        context['breadcrums'] = breadcrums
        context['actions'] = []

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
