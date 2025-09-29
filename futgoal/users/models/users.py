import math
from datetime import datetime

from django.db.models import Sum
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import translation
from django.db.models import Q
from django.contrib.auth.models import Group

import hashlib
from random import choice

from futgoal.configuration.models import Configuration


def random_digits(number_digits=6):
    import random
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(number_digits):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    return random_str


def md5_generate(n=20, en_md5=True):
    valores = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+'
    p = ''
    p = p.join([choice(valores) for i in range(n)])
    if en_md5:
        p = hashlib.md5(p.encode()).hexdigest()
    return p


class User(AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    remember_key = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        verbose_name=_("Clave de recuperación de contraseña"),
    )

    position = models.CharField(
        blank=True,
        null=True,
        max_length=140,
        verbose_name=_("Cargo que ocupa"),
    )

    pre_email = models.CharField(_("Pre Email"), max_length=140, null=True, blank=True)

    full_name = models.CharField(_("Nombre Completo"), max_length=140, null=True, blank=True)

    uuid = models.CharField(
        blank=True,
        null=True,
        max_length=36,
        verbose_name=_("UUID"),
    )


    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ["email"]

    def __str__(self):
        return self.full_name

    @property
    def magic_login_link(self):
        return f"https://futgoal.adammartin.es/es/auth/loginwithuuid/{self.uuid}/"

    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = md5_generate()
        self.username = self.email
        if not self.remember_key:
            self.remember_key = md5_generate()
        if not self.pre_email:
            self.pre_email = self.email.split('@')[0]
        self.full_name = f"{self.first_name} {self.last_name}"

        super(User, self).save(*args, **kwargs)

    def add_action(self, action_description):
        from futgoal.users.models import ActionLogUser
        ActionLogUser.objects.create(
            user=self, action_description=action_description
        )

    def update_remember_key(self):
        self.remember_key = md5_generate()
        self.save()

    def send_welcome_email(self):
        from django.conf import settings
        from futgoal.configuration.models import Configuration

        configuration = Configuration.objects.first()

        self.update_remember_key()
        remember_url = settings.SITE_URL + reverse(
            "auth:type_your_password", kwargs={"remember_key": self.remember_key}
        )

        context = {
            "remember_url": remember_url,
            "app_name": configuration.app_name,
        }
        body_html = render_to_string(
            "emails/users/welcome_email.html", context)
        context = {
            "content": body_html,
            "preheader": _("Establecer contraseña"),
            "app_name": configuration.app_name,
        }
        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("{} - Nueva cuenta de usuario".format(configuration.app_name)),
            from_email,
            self.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.add_action(_("Welcome email"))

        if configuration.enable_emails:
            return msg.send(fail_silently=False)
        else:
            return True

    def send_email_remember_password(self):
        from futgoal.configuration.models import Configuration

        configuration = Configuration.objects.first()

        self.update_remember_key()
        remember_url = settings.SITE_URL + reverse(
            "auth:type_your_password", kwargs={"remember_key": self.remember_key}
        )

        context = {
            "remember_url": remember_url,
            "app_name": configuration.app_name,
        }
        body_html = render_to_string(
            "emails/users/remember_password.html", context)
        context = {
            "content": body_html,
            "preheader": _("Recordar contraseña"),
            "app_name": configuration.app_name,
        }
        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("{} - Cambio de contraseña".format(configuration.app_name)),
            from_email,
            self.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.add_action(_("Reset password email"))

        if configuration.enable_emails:
            msg.send(fail_silently=False)
