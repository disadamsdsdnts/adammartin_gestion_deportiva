from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        """
        Personaliza los mensajes de allauth, especialmente el de login exitoso
        """
        # Si es el mensaje de login exitoso, lo personalizamos
        if message_template == 'account/messages/signed_in.txt':
            user = request.user
            if user and user.is_authenticated:
                custom_message = _('Sesión iniciada correctamente como %(email)s') % {'email': user.email}
                messages.add_message(request, level, custom_message, extra_tags=extra_tags)
                return

        # Para otros mensajes, usar el comportamiento por defecto
        super().add_message(request, level, message_template, message_context, extra_tags)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Este método se ejecuta antes de que se complete el login social.
        Aquí verificamos si existe un usuario con el email proporcionado por Google.
        Si existe, vinculamos la cuenta social con el usuario existente.
        """
        # El email del usuario que intenta iniciar sesión con Google
        email = sociallogin.account.extra_data.get('email')

        if email:
            # Intentamos encontrar un usuario existente con ese email
            try:
                user = User.objects.get(email=email)
                # Si el usuario existe pero no está vinculado a la cuenta social,
                # lo vinculamos
                if not sociallogin.is_existing:
                    sociallogin.connect(request, user)
            except User.DoesNotExist:
                messages.add_message(
                    request,
                    messages.WARNING,
                    _('Usuario no encontrado')
                )
                return HttpResponseRedirect(reverse('dashboard'))
