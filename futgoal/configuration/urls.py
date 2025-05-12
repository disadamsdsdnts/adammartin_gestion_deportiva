from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ConfigurationUpdateView,
    ConfigurationDetailView,
)

urlpatterns = [
    path("configuration/", ConfigurationDetailView.as_view(),
         name="configuration_detail"),
    path("configuration/update/",
         ConfigurationUpdateView.as_view(), name="configuration_update"),
]
