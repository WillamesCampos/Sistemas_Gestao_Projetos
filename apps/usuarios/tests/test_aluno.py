from uuid import uuid4
from rest_framework import status

from apps.usuarios.tests.test_login import TestCore
from apps.usuarios.tests.factory.usuarios import AlunoFactory
from apps.usuarios.models import Aluno


class TestAluno(TestCore):

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_criar_aluno(self):
        """
            - Motivação:
                - Criar um aluno.
            - Regra de negócio:
                - O usuário deve informar e-mail, nome e senha
                - O e-mail informado não deve estar associado a outro usuário
            - Resultado Esperado:
                - status: 201
        """

        data = {
            'nome': 'Aluno de Teste',
            'matricula': '20220043789',
            'senha': '123',
            'email': 'aluno_de_teste@teste.com'
        }

        url = '/alunos/'
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.data['matricula'],
            data['matricula']
        )

    def test_criar_aluno_sem_senha(self):
        """
            - Motivação:
                - Criar um aluno sem informar a senha.
            - Regra de negócio:
                - Não pode ser criado um aluno sem informar a senha
            - Resultado Esperado:
                - status: 400
        """

        data = {
            'nome': 'Aluno de Teste',
            'matricula': '20220043789',
            'email': 'aluno_de_teste@teste.com'
        }

        url = '/alunos/'
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data['senha'][0],
            'Este campo é obrigatório.'
        )

    def test_criar_aluno_sem_email(self):
        """
            - Motivação:
                - Criar um aluno sem informar o e-mail.
            - Regra de negócio:
                - Para criar um usuário aluno, deve ser
                informado o e-mail.
            - Resultado Esperado:
                - status: 400
        """

        data = {
            'nome': 'Aluno de Teste',
            'matricula': '20220043789',
            'senha': '123',
        }

        url = '/alunos/'
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data['email'][0],
            'Este campo é obrigatório.'
        )

    def test_criar_aluno_sem_nome(self):
        """
            - Motivação:
                - Criar um aluno sem informar o nome.
            - Regra de negócio:
                - Para criar o usuário aluno, o nome deve
                ser obrigatoriamente informado.
            - Resultado Esperado:
                - status: 400
        """

        data = {
            'matricula': '20220043789',
            'senha': '123',
            'email': 'aluno_de_teste@teste.com'
        }

        url = '/alunos/'
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data['nome'][0],
            'Este campo é obrigatório.'
        )

    def test_criar_aluno_sem_matricula(self):
        """
            - Motivação:
                - Criar um aluno sem informar a matrícula.
            - Regra de negócio:
                - Não é possível criar um usuário aluno sem
                informar uma matrícula.
            - Resultado Esperado:
                - status: 400
        """

        data = {
            'nome': 'Aluno de Teste',
            'senha': '123',
            'email': 'aluno_de_teste@teste.com'
        }

        url = '/alunos/'
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data['matricula'][0],
            'Este campo é obrigatório.'
        )

    def test_editar_nome_aluno(self):
        """
            - Motivação:
                - Editar o nome de um aluno.
            - Regra de negócio:
                - O campo nome deve ser informado.
            - Resultado Esperado:
                - status: 200
        """

        data = {
            'nome': 'Aluno de Testes'
        }

        url = f'/alunos/{self.aluno.codigo}/'
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.aluno.refresh_from_db()

        self.assertEqual(
            response.data['nome'],
            self.aluno.nome
        )

    def test_editar_email_aluno(self):
        """
            - Motivação:
                - Editar o e-mail do aluno.
            - Regra de negócio:
                - O e-mail informado não deve estar associado a outro usuário
            - Resultado Esperado:
                - status: 200
        """

        data = {
            'email': 'outro_email_aluno@teste.com'
        }

        url = f'/alunos/{self.aluno.codigo}/'
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.aluno.refresh_from_db()

        self.assertEqual(
            response.data['email'],
            self.aluno.email
        )

    def test_editar_matricula_aluno(self):
        """
            - Motivação:
                - Editar a matrícula do aluno.
            - Regra de negócio:
                - A matrícula informada não deve estar associado a outro
                usuário.
            - Resultado Esperado:
                - status: 200
        """

        data = {
            'matricula': '202320034323'
        }

        url = f'/alunos/{self.aluno.codigo}/'
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.aluno.refresh_from_db()

        self.assertEqual(
            response.data['matricula'],
            self.aluno.matricula
        )

    def test_editar_matricula_existente_aluno(self):
        """
            - Motivação:
                - Editar a matrícula do aluno por outra já cadastrada.
            - Regra de negócio:
                - Não é possível alterar a matrícula do aluno por
                outra que pertence a outro usuário aluno.
            - Resultado Esperado:
                - status: 400
        """

        data = {
            'matricula': self.aluno.matricula
        }

        url = f'/alunos/{str(self.aluno.codigo)}/'
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.aluno.refresh_from_db()

    def test_remover_aluno(self):
        """
            - Motivação:
                - Remover um aluno.
            - Regra de negócio:
                - O código informado na URL deve corresponder a
                um aluno.
            - Resultado Esperado:
                - status: 204
        """

        aluno = AlunoFactory()

        url = f'/alunos/{aluno.codigo}/'
        response = self.client.delete(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_remover_aluno_codigo_invalido(self):
        """
            - Motivação:
                - Remover um aluno informando código não associado
                a nenhum aluno cadastrado.
            - Regra de negócio:
                - O código informado na URL deve corresponder a
                um aluno.
            - Resultado Esperado:
                - status: 404
        """

        url = f'/alunos/{str(uuid4())}/'
        response = self.client.delete(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_listar_alunos(self):
        """
            - Motivação:
                - Listar todos os alunos cadastrados.
            - Regra de negócio:
                - Todos os alunos cadastrados são exibidos.
            - Resultado Esperado:
                - status: 200
                - paginação
        """

        AlunoFactory.create_batch(
            size=12
        )

        url = '/alunos/'
        response = self.client.get(
            url
        )

        quantidade_alunos = Aluno.objects.count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        assert response.data['quantidade'] == quantidade_alunos

        assert all(
            key_response in self.pagination_keys for key_response in response.data.keys() # noqa
        )
