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
from futgoal.users.views.user_views import UserProfileView
from futgoal.users.views.onboarding_views import (
    OnboardingWelcomeView,
    OnboardingTeamView,
    OnboardingSeasonView,
    OnboardingCompleteView,
)


urlpatterns = [
    path(
        '',
        DashboardView.as_view(),
        name='dashboard'
    ),

    path('404/', Error404View.as_view()),

    path('admin/', admin.site.urls),

    # URL de perfil directa
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Onboarding URLs (en root para que DashboardView pueda acceder sin namespace)
    path('onboarding/', OnboardingWelcomeView.as_view(), name='onboarding_welcome'),
    path('onboarding/team/', OnboardingTeamView.as_view(), name='onboarding_team'),
    path('onboarding/season/', OnboardingSeasonView.as_view(), name='onboarding_season'),
    path('onboarding/complete/', OnboardingCompleteView.as_view(), name='onboarding_complete'),

    path('auth/',
         include(('futgoal.users.urls.user_auth_urls', 'users'),
                 namespace='auth')
         ),

    # django-allauth URLs
    path('accounts/', include('allauth.urls')),

    path('',
         include(('futgoal.users.urls', 'users'),
                 namespace='users')
         ),

    path('players/',
         include(('futgoal.players.urls', 'players'),
                 namespace='players')
         ),

    path('config/',
         include(('futgoal.configuration.urls', 'configuration'),
                 namespace='configuration')
         ),

    path('team/',
         include(('futgoal.team.urls', 'team'),
                 namespace='team')
         ),

    path('season/',
         include(('futgoal.season.urls', 'season'),
                 namespace='season')
         ),

    path('matches/',
         include(('futgoal.matches.urls', 'matches'),
                 namespace='matches')
         ),

    path('rivals/',
         include(('futgoal.rivals.urls', 'rivals'),
                 namespace='rivals')
         ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Django Browser Reload
if "django_browser_reload" in settings.INSTALLED_APPS:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

admin.site.index_title = "FutGOAL"
admin.site.site_header = "FutGOAL"
admin.site.site_title = "FutGOAL"
