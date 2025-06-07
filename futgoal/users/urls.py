# -*- encoding: utf-8 -*-

"""Users urls."""

from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from futgoal.users.views import (
    DashboardView,
    LoginView,
    logout_view,
    RememberPassword,
    TypeYourPassword,
    RememberEmailSended,
)
from futgoal.users.views.user_views import UserProfileView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('reset-password/', RememberPassword.as_view(), name='remember_password_form'),
    re_path('reset-password/type-your-password/(?P<remember_key>[0-9a-f]{32})/', TypeYourPassword.as_view(), name='type_your_password'),
    path('reset-password/email-sended/', RememberEmailSended.as_view(), name='remember_password_email_sended'),
]
