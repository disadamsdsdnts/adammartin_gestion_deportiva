from io import BytesIO
import re
import datetime


from django.views.generic import (
    FormView,
    DetailView,
    UpdateView,
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from futgoal.configuration.forms import ConfigurationUpdateForm
from futgoal.configuration.models import Configuration

from futgoal.users.models import User
