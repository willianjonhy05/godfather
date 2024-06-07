from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Perfil

class PerfilModelTest(TestCase):

    def setUp(self):
        self.perfil_data = {
            'email': 'testuser@example.com',
            'telefone': '12345678901',
            'nome': 'Test User'
        }

    def test_gerar_username_automaticamente(self):
        perfil = Perfil.objects.create(
            email='nousername@example.com',
            telefone='12345678901',
            nome='No Username'
        )
        

        self.assertIsNotNone(perfil.username)
        self.assertTrue(perfil.username.startswith('nousername'.split('@')[0]))
        self.assertEqual(len(perfil.username), len('nousername'.split('@')[0]) + 4)  # Verifica se tem 4 dígitos adicionais

    def test_username_nao_gerado_se_fornecido(self):
        perfil = Perfil.objects.create(
            username='fornecido',
            email='fornecido@example.com',
            telefone='12345678902',
            nome='Fornecido User'
        )

        self.assertEqual(perfil.username, 'fornecido')

