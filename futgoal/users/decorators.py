from django.utils.decorators import method_decorator
from functools import wraps
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404

from futgoal.users.models import User



class is_global_admin(object):

    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)

    def __call__(self, request, *args, **kwargs):
        response = self.view_func(request, *args, **kwargs)
        if request.user and request.user.is_superuser:
            return response
        raise PermissionDenied



class is_global_user(object):

    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)

    def __call__(self, request, *args, **kwargs):
        response = self.view_func(request, *args, **kwargs)
        if request.user and (request.user.is_eveon_user or request.user.is_superuser):
            return response
        raise PermissionDenied
