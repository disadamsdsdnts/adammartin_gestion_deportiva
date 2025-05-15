from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from futgoal.sales.models import Ranking, Sale

#reverse_lazy
from django.urls import reverse_lazy

from django.contrib import messages

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)

from futgoal.users.decorators import (
    is_global_admin,
    is_support
)

from futgoal.users.forms import LoginForm, RememberForm, PasswordForm, LoginCodeForm
from futgoal.users.models import User
from futgoal.sales.forms import SaleSuUpdateForm

from django.db.models import Sum, Count

decorators = [
    csrf_protect,
    never_cache,
]


@method_decorator([login_required, is_support], name='dispatch')
class SuDashboardView(TemplateView):
    template_name = 'dashboards/su/SuDashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        breadcrumbs = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
        ]
        context['page_title'] = 'Dashboard de Soporte'
        context['breadcrumbs'] = breadcrumbs
        context['js_template'] = ['js/custom/datatables.js']

        return context



@method_decorator([login_required, is_support], name='dispatch')
class SuListView(ListView):
    model = Sale
    template_name = 'support/SuList.html'
    context_object_name = 'sales'

    def get_queryset(self):
        queryset = super().get_queryset().filter(sale_type__in=['NV','NVF','RNV']).select_related('product')

        if self.request.user.groups.filter(name='Soporte Conquer Blocks').exists():
          queryset = queryset.filter(product__school='CB')

        if self.request.user.groups.filter(name='Soporte FI').exists():
          queryset = queryset.filter(product__school='CF')

        if self.request.GET.get('month'):
            month = int(self.request.GET.get('month'))
        else:
            month = datetime.now().month

        if month != 0:
            queryset = queryset.filter(date__month=month)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Onboarding'), 'url': reverse(
                'support:su_list')},
        ]
        context['page_title'] = _('Onboarding')

        context['breadcrumbs'] = breadcrumbs
        context['js_template'] = ['js/custom/datatables.js']

        months_original = [
            ('0', 'Todos'),
            ('1', 'Enero'),
            ('2', 'Febrero'),
            ('3', 'Marzo'),
            ('4', 'Abril'),
            ('5', 'Mayo'),
            ('6', 'Junio'),
            ('7', 'Julio'),
            ('8', 'Agosto'),
            ('9', 'Septiembre'),
            ('10', 'Octubre'),
            ('11', 'Noviembre'),
            ('12', 'Diciembre')
        ]

        queryset = Sale.objects.filter(sale_type__in=['NV','NVF','RNV']).select_related('product')

        # Si tiene los dos no filtramos
        if self.request.user.groups.filter(name='Soporte Conquer Blocks').exists() and self.request.user.groups.filter(name='Soporte FI').exists():
          queryset = queryset
        else:
          # Si tiene uno de los dos filtramos
          if self.request.user.groups.filter(name='Soporte Conquer Blocks').exists():
            queryset = queryset.filter(product__school='CB')

          if self.request.user.groups.filter(name='Soporte FI').exists():
            queryset = queryset.filter(product__school='CF')

        months_with_sales = queryset.dates('date', 'month', order='DESC').values_list('date__month', flat=True)

        # Ahora elimina de months los meses que no tienen ventas
        months_for_menu = [month for month in months_original if int(month[0]) in months_with_sales]
        context['months_for_menu'] = months_for_menu

        # Ahora vamos a ver qué mes estamos viendo
        month_selected = int(self.request.GET.get('month', datetime.now().month))
        context['current_month'] = months_original[month_selected][1]
        context['current_month_number'] = months_original[month_selected][0]

        context['sales_without_contact'] = self.get_queryset().filter(support_contacted_date__isnull=True)
        context['sales_contacted'] = self.get_queryset().exclude(support_contacted_date__isnull=True)

        return context


@method_decorator([login_required, is_support], name='dispatch')
class SuUpdateView(UpdateView):
    form_class = SaleSuUpdateForm
    model = Sale
    template_name = 'sales/SaleSuUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
            {'title': _('Editar venta'), 'url': ''}
        ]
        context['page_title'] = _('Editar venta')
        context['breadcrumbs'] = breadcrumbs
        return context


    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Venta actualizado correctamente')
        )

        return reverse_lazy(
            'support:su_list'
        )

@method_decorator([login_required, is_support], name='dispatch')
class SuDetailView(DetailView):
    template_name = 'sales/SaleSuDetail.html'
    model = Sale

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = [
            {'title': _('Dashboard'), 'url': reverse('dashboard')},
        ]
        context['page_title'] = _('Venta')
        context['breadcrumbs'] = breadcrumbs
        return context
