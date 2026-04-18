from django.test import TestCase
from django.urls import reverse


class LeituraPagesTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar em Programador Pragmático")

    def test_programador_pragmatico_page_loads(self):
        response = self.client.get(reverse("programador_pragmatico"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resumos de capítulos")
