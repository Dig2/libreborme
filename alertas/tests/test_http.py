from django.core.management import call_command
from django.conf import settings
from django.urls import reverse

from django.test.client import Client
from django.test import TestCase

from alertas.utils import create_alertas_user


class TestAlertasHttp(TestCase):

    fixtures = ['alertasconfig.json']

    def setUp(self):
        super(TestAlertasHttp, self).setUp()
        self.user = create_alertas_user("fred@localhost", "secret", "Fred", "Foo")
        self.client = Client()
        self.client.login(email='fred@localhost', password='secret')

    def test_index(self):
        url = reverse('dashboard-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestAlertasLoginRequired(TestCase):

    def setUp(self):
        self.login_url = settings.LOGIN_URL
        # self.client = Client()

    def test_alertas(self):
        url = reverse('dashboard-index')
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_profile(self):
        url = reverse('alertas-profile')
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_id(self):
        url = reverse('alertas-detail', args=['1'])
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_ayuda(self):
        url = reverse('alertas-ayuda')
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_billing(self):
        url = reverse('alertas-billing')
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_history(self):
        url = reverse('alertas-history')
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_history_download(self):
        url = reverse('alerta-history-download', args=['1'])
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_new_acto(self):
        url = reverse('alertas-new-acto')
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_remove_acto(self):
        url = reverse('alerta-remove-acto', args=['1'])
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_ajax_suggest_company(self):
        url = reverse('suggest_company')
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_alertas_ajax_suggest_person(self):
        url = reverse('suggest_person')
        response = self.client.get(url)
        self.assertTrue(response.url.startswith(self.login_url))
