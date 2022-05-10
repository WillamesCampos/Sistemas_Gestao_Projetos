from rest_framework import status
from apps.usuarios.tests.test_login import TestCore
from apps.turmas.tests.factory.turmas import Disciplina, DisciplinaFactory


class TestDisciplina(TestCore):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        response = cls.client.post(
            '/login/',
            data={
                'username': cls.professor.email,
                'password': '123'
            }
        )

        cls.token = f'Token {response.data.get("token")}'
        cls.client.credentials(
            HTTP_AUTHORIZATION=cls.token
        )

    def test_listar_disciplinas(self):

        DisciplinaFactory(
            professor=self.professor
        )

        url = '/disciplinas/'

        response = self.client.get(
            url
        )

        disciplinas_professor = Disciplina.objects.filter(
            professor=self.professor
        ).count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['quantidade'],
            disciplinas_professor
        )

    def test_criar_disciplina(self):

        url = '/disciplinas/'

        data = {
            'nome': 'Disciplina A',
            'nota_corte': 7,
            'quantidade_grupos': 4
        }

        response = self.client.post(
            url, data=data
        )

        disciplina_professor = Disciplina.objects.get(
            professor=self.professor,
            nome=data['nome']
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data['codigo'],
            disciplina_professor.codigo
        )

    def test_editar_disciplina(self):

        disciplina = DisciplinaFactory(
            professor=self.professor
        )

        url = f'/disciplinas/{str(disciplina.codigo)}/'

        data = {
            'quantidade_grupos': 4
        }

        response = self.client.patch(
            url, data=data
        )

        disciplina.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            disciplina.quantidade_grupos,
            response.data['quantidade_grupos']
        )

    def test_desativar_disciplina(self):

        disciplina = DisciplinaFactory(
            professor=self.professor
        )

        url = f'/disciplinas/{str(disciplina.codigo)}/'

        response = self.client.delete(
            url
        )

        disciplina.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(disciplina.ativo)