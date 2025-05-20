from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ConfigurationUpdateView,
)

urlpatterns = [
    path("configuration/",
         ConfigurationUpdateView.as_view(), name="configuration_update"),
]
