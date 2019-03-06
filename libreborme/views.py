from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic.base import TemplateView

from djstripe.models import Plan

from borme.mixins import CacheMixin
from alertas.utils import get_alertas_config
from . import utils

from pathlib import Path


import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class AvisoLegalView(CacheMixin, TemplateView):
    template_name = "libreborme/aviso_legal.html"

    def get_context_data(self, **kwargs):
        context = super(AvisoLegalView, self).get_context_data(**kwargs)
        context['lopd'] = settings.LOPD
        return context


class AboutView(CacheMixin, TemplateView):
    template_name = "libreborme/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['HOST_BUCKET'] = settings.HOST_BUCKET
        return context


class ServicesView(CacheMixin, TemplateView):
    template_name = "libreborme/services.html"

    def get_context_data(self, **kwargs):
        context = super(ServicesView, self).get_context_data(**kwargs)

        aconfig = get_alertas_config()
        context["service_api_free_req_day"] = aconfig["service_api_free_req_day"]
        context["service_api_advanced_req_day"] = aconfig["service_api_advanced_req_day"]
        context["max_alertas_follower_free"] = aconfig["max_alertas_follower_free"]
        context["max_alertas_follower_paid"] = aconfig["max_alertas_follower_paid"]

        context["plan_subscription_month_one"] = Plan.objects.get(nickname=settings.SUBSCRIPTION_MONTH_ONE_PLAN)
        context["plan_subscription_month_full"] = Plan.objects.get(nickname=settings.SUBSCRIPTION_MONTH_FULL_PLAN)
        context["plan_api_month"] = Plan.objects.get(nickname=settings.API_MONTH_PLAN)
        plan_follow_year = Plan.objects.get(nickname=settings.ALERTS_YEAR_PLAN)
        context["plan_follow_month_price"] = plan_follow_year.amount / 12

        return context


def robotstxt(request):
    """Check if static robots.txt exists, otherwise return default template"""
    response = None
    static_root = settings.STATIC_ROOT
    if static_root is not None:
        filename = Path(static_root) / "robots.txt"
        if filename.exists():
            with open(filename.as_posix()) as fp:
                response = fp.read()

    if response is None:
        template = get_template('robots.txt')
        response = template.render()

    return HttpResponse(response, content_type='text/plain')


# XXX: Do we really need this?
"""Creates new invoice (LBInvoice)

Set the following fields: start_date, end_date, amount, payment_type
name, email, address, ip, subscription_id and nif (TODO)
"""
"""
def create_new_invoice(request, customer, subscription, plan, user_input):
    new_invoice = LBInvoice(user=request.user)
    new_invoice.start_date = subscription.current_period_start
    new_invoice.end_date = subscription.current_period_end
    new_invoice.amount = plan.amount
    new_invoice.payment_type = 'stripe'
    new_invoice.name = user_input["name"]
    new_invoice.email = user_input["email"]
    new_invoice.address = ", ".join([user_input["address"],
                                     user_input["zipcode"],
                                     user_input["state"],
                                     user_input["city"],
                                     user_input["country"]])
    new_invoice.ip = request.META.get('HTTP_X_FORWARDED_FOR',
                                      request.META['REMOTE_ADDR'])
    new_invoice.subscription_id = subscription.id
    new_invoice.nif = customer.business_vat_id or "TODO"
    return new_invoice
"""
