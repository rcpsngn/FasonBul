"""
fasonbul/tests.py — Proje düzeyinde temel sistem testleri.
"""

from django.test import TestCase, Client
from django.urls import reverse


class SystemCheckTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ana_sayfa_erisilebilir(self):
        """Ana sayfanın (index) 200 HTTP kodu ile yanıt verip vermediğini kontrol eder."""
        response = self.client.get(reverse('mainpage:index'))
        self.assertEqual(response.status_code, 200)

    def test_admin_paneli_yonlendirmesi(self):
        """Admin paneline erişim isteğinin başarılı olduğunu kontrol eder."""
        response = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(response.status_code, 200)