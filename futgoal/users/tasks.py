from celery import shared_task
from futgoal.celery import app as celery_app
import datetime

# import the logging library
import logging

from futgoal.users.models import User


# Get an instance of a logger
logger = logging.getLogger(__name__)


@celery_app.task
def send_welcome_email(user_pk):
    """ Tarea que se encargará de enviar un email de bienvenida"""

    logger.info(
        "Comienzo de envío de mail de bienvenida para el usuario: {}".format(
            user_pk)
    )
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        logger.error("Usuario no encontrado con pk: %s" % user_pk)
        return 1

    user.send_welcome_email()


@celery_app.task
def send_email_remember_password(user_pk):
    """ Tarea que se encargará de enviar un email de recordar contraseña """

    logger.info(
        "Comienzo de envío de mail de recordar contraseña para el usuario: {}".format(
            user_pk
        )
    )
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        logger.error("Usuario no encontrado con pk: %s" % user_pk)
        return 1

    user.send_email_remember_password()
