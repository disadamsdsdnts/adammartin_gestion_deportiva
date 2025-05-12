from django.urls import reverse_lazy

from django.conf import settings
from futgoal.configuration.models import Configuration


def get_menu_urls(request, pk=None):
    if 'pk' in request.resolver_match.kwargs:
        pk = request.resolver_match.kwargs['pk']
    users_urls = [
        reverse_lazy('users:ga_user_list'),
        reverse_lazy('users:ga_user_create'),
    ]

    if pk is not None:
        users_urls = users_urls + [
            reverse_lazy(
                'users:ga_user_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'users:ga_user_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'users:ga_user_delete',
                kwargs={'pk': pk}
            )
        ]

    return {
        'USERS_URLS': users_urls,
        'DEV': settings.DEV,
        'DEVJS': settings.DEVJS,
        'CONFIGURATION': Configuration.objects.first()
    }
