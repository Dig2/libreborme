"""
https://stripe.com/docs/api/events/types

Docs:
https://github.com/dj-stripe/dj-stripe/issues/791
https://github.com/dj-stripe/dj-stripe/issues/782
https://github.com/dj-stripe/dj-stripe/issues/419

https://stackoverflow.com/questions/19161630/how-to-prevent-manage-stripe-webhook-sending-invoice-for-0-on-trial-signup
https://stackoverflow.com/questions/19467287/stripe-how-to-handle-subscription-with-a-free-plan-and-no-credit-card-required
"""
from django.core.mail import mail_admins

from djstripe import webhooks
from djstripe.models import Subscription

import stripe
import datetime


@webhooks.handler("customer.subscription.created")
def customer_subscription_created(event, **kwargs):
    """
    Notify to admins
    """
    print("Webhook " + event.type)
    now = datetime.datetime.now()
    user = event.customer.subscriber
    full_name = user.get_full_name()
    subject = 'Libreborme webhook triggered: ' + event.type
    message = """\
Nueva suscripción

El {} se ha suscrito al usuario {} ({})
""".format(
        now.strftime("%c"), full_name, user.email)
    mail_admins(subject, message)


@webhooks.handler("customer.subscription.updated")
def customer_subscription_updated(event, **kwargs):
    """
    For example when user has cancelled his subscription.
    Notify to admins
    """
    print("Webhook " + event.type)
    now = datetime.datetime.now()
    user = event.customer.subscriber
    full_name = user.get_full_name()
    subject = 'Libreborme webhook triggered: ' + event.type
    message = """\
Cambio en la suscripción

El {} se ha producido un cambio en el suscriptor {} ({}).

Cambios:
{}
""".format(
        now.strftime("%c"), full_name, user.email, event.data['previous_attributes'])
    mail_admins(subject, message)


@webhooks.handler("customer.subscription.deleted")
def customer_subscription_deleted(event, **kwargs):
    """
    Workaround for issue: https://github.com/dj-stripe/dj-stripe/issues/855

    When a subscription is finally canceled or 'right now' using the dashboard,
    it is also removed from DB due to a nasty bug

    Re-sync again and mark UserSubscription as disabled
    """
    print("Webhook " + event.type)
    obj_id = event.data['object']['id']
    stripe_subscription = stripe.Subscription.retrieve(obj_id)
    djstripe_subscription = Subscription.sync_from_stripe_data(stripe_subscription)

    # TODO: set is_enabled = False
    # Since it was removed, there is no link to subscription
    # subscription = djstripe_subscription.lb_subscription.get()
    # subscription.is_enabled = False
    # subscription.save()
    now = datetime.datetime.now()
    user = event.customer.subscriber
    full_name = user.get_full_name()
    subject = 'Libreborme webhook triggered: ' + event.type
    message = """\
Suscripción cancelada

El {} se canceló la suscripción del usuario {} ({})
""".format(
        now.strftime("%c"), full_name, user.email)
    mail_admins(subject, message)


# https://stripe.com/docs/recipes/sending-emails-for-failed-payments
@webhooks.handler("invoice.payment_failed")
def invoice_payment_failed(event, **kwargs):
    """
    Notify to admins and user
    """
    print("Webhook " + event.type)
    now = datetime.datetime.now()
    user = event.customer.subscriber
    full_name = user.get_full_name()
    subject = 'Libreborme webhook triggered: ' + event.type
    message = """\
Pago fallido

El {} ha fallado al cobrar al usuario {} ({})
""".format(
        now.strftime("%c"), full_name, user.email)
    mail_admins(subject, message)

    # TODO: Usar MailTemplate's
    subject = "Tu último pago ha fallado"
    message = """No hemos podido hacer el cargo de la última factura de %(amount) euros.
Esto puede ser debido a un cambio en el número de tu tarjeta o a que la tarjeta ha expirado o ha sido cancelada.

Por favor actualiza tu método de pago tan pronto como sea posible para que no interrumpamos el servicio.

%(url) métodos de pago
"""
    user.email_user(
        subject=subject,
        message=message
    )


@webhooks.handler("invoice.upcoming")
def invoice_upcoming(event, **kwargs):
    """
    Notify to admins for review
    """
    print("Webhook " + event.type)
    now = datetime.datetime.now()
    user = event.customer.subscriber
    full_name = user.get_full_name()
    subject = 'Libreborme webhook triggered: ' + event.type
    message = """\
Borrador de factura

El {} se ha generado un borrador de factura para el usuario {} ({}).
¡Revísala!
""".format(
        now.strftime("%c"), full_name, user.email)
    mail_admins(subject, message)


@webhooks.handler("customer.created")
def customer_created(event, **kwargs):
    """
    Notify to admins
    """
    print("Webhook " + event.type)
    now = datetime.datetime.now()
    customer = event.customer
    # FIXME: If created thru the Stripe dashboard, user won't exist
    # user = event.customer.subscriber
    # full_name = user.get_full_name()
    subject = 'Libreborme webhook triggered: ' + event.type
    message = """\
Nuevo customer

El {} se ha creado un nuevo customer {}.
""".format(
        now.strftime("%c"), customer.email)
    mail_admins(subject, message)


@webhooks.handler("customer.subscription.trial_will_end")
def customer_subscription_trial_will_end(event, **kwargs):
    """
    Sent three days before the trial period is up
    Notify user
    """
    user = event.customer.subscriber

    # TODO: Usar MailTemplate's
    # TODO: redactar
    subject = "Tu periodo de prueba va a finalizar pronto"
    message = """Blablabla... upcoming invoice día y cantidad
"""
    # user.email_user(
    #     subject=subject,
    #     message=message
    # )


@webhooks.handler("charge.succeeded")
def charge_succeeded(event, **kwargs):
    """
    Sent by Stripe one hour after invoice.created
    Notify to admins
    """
    print("Webhook " + event.type)
    now = datetime.datetime.now()
    user = event.customer.subscriber
    full_name = user.get_full_name()
    subject = 'Libreborme webhook triggered: ' + event.type
    message = """\
Pago realizado

El {} se ha realizado un pago con éxito del customer {} ({}).
""".format(
        now.strftime("%c"), full_name, user.email)
    mail_admins(subject, message)


"""
@webhooks.handler("customer")
def customer_created(event, **kwargs):
    print("Webhook " + event.type)
    subject = 'Webhook: ' + event.type
    message = '%r\n' % (event)
    mail_admins(subject, message)
"""
