# -*- encoding: utf-8 -*-

"""Team urls."""

from django.urls import path

from .views import TeamDetailView, TeamUpdateView

urlpatterns = [
    path(
        '',
        TeamDetailView.as_view(),
        name='detail'
    ),
    path(
        'update/',
        TeamUpdateView.as_view(),
        name='update'
    ),
]
