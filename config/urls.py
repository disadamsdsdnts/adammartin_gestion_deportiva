"""Main URLs module."""

from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from futgoal.users.views import (
    DashboardView,
    Error404View
)


urlpatterns = [
    path(
        '',
        DashboardView.as_view(),
        name='dashboard'
    ),

    path('404/', Error404View.as_view()),

    path('admin/', admin.site.urls),

    path('auth/',
         include(('futgoal.users.urls.user_auth_urls', 'users'),
                 namespace='auth')
         ),

    # django-allauth URLs
    path('accounts/', include('allauth.urls')),

    path('users/',
         include(('futgoal.users.urls.user_urls', 'users'),
                 namespace='users')
         ),

    path('config/',
         include(('futgoal.configuration.urls', 'configuration'),
                 namespace='configuration')
         ),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

admin.site.index_title = "FutGOAL"
admin.site.site_header = "FutGOAL"
admin.site.site_title = "FutGOAL"
