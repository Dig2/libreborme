#!/usr/bin/env python3
#
# Example usage:
# 	./manage.py expire_test_users
#
# Expire a specific user without having into account date
# 	./manage.py expire_test_users --username user
#
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template import loader

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

from alertas.email import send_expiration_email
from alertas.models import Profile
from alertas.utils import get_alertas_config

from django.utils import timezone
import logging
import os.path

LOG = logging.getLogger(__file__)
LOG.setLevel(logging.INFO)

EMAIL_FROM = "noreply@libreborme.net"
EMAIL_TEMPLATES_PATH = os.path.join("alertas", "templates", "email")
NOTIFICATION_SUBJECT = "Su período de pruebas en Libreborme Alertas ha expirado"
EXPIRE_AFTER_DAYS = int(get_alertas_config("days_test_subscription_expire"))


class Command(BaseCommand):
    help = 'Expire test accounts after {0} days of creation'.format(EXPIRE_AFTER_DAYS)

    def add_arguments(self, parser):
        parser.add_argument("--username")
        parser.add_argument("--silent", action='store_true', default=False, help="Do not send email to the user")

    def handle(self, *args, **options):
        ch = logging.StreamHandler()
        if options["verbosity"] > 1:
            LOG.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)
        LOG.addHandler(ch)

        if options['username']:
            user = User.objects.get(username=options["username"])
            if user.is_active:
                expire_user(user, options["silent"])
            else:
                print("User is already inactive")
        else:
            # Find users that joined days_test_subscription_expire days ago and more
            date = timezone.now() - timezone.timedelta(days=EXPIRE_AFTER_DAYS)
            users = User.objects.filter(profile__account_type='test', date_joined__lte=date, is_active=True)
            if len(users) > 0:
                for user in users:
                    expire_user(user, options["silent"])
            else:
                print("No test users found to expire")


def expire_user(user, silent):
    print("Expiring test user: {0} ({1})".format(user.username, user.email))
    user.profile.expire_subscription(send_email=not silent)
