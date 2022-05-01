from django.contrib.auth.hashers import check_password

from apps.usuarios.models import Professor
from .test_login import TestCore
from rest_framework import status


class TestProfessor(TestCore):

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

    def test_cadastrar_professor(self):
        """
            - Motivação:
                - Criar um professor.
            - Regra de negócio:
                - O usuário deve informar e-mail, nome e senha
                - O e-mail informado não deve estar associado a outro usuário
            - Resultado Esperado:
                - status: 201
        """

        url = '/professores/'
        data = {
            'nome': 'Professor Teste 2',
            'email': 'novo_professor@teste.com',
            'senha':'teste'
        }
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        assert ( response.data[key] == data[key] for key in response.data.keys())

    def test_cadastrar_professor_sem_senha(self):
        """
            - Motivação:
                - Criar um professor sem informar senha
            - Regra de negócio:
                - O usuário que informar e-mail e senha corretamente,
                receberá o token de acesso da aplicação.
            - Resultado Esperado:
                - status: 400
        """

        url = '/professores/'
        data = {
            'nome': 'Professor Teste 2',
            'email': 'novo_professor@teste.com'
        }
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_cadastrar_professor_sem_nome(self):
        """
            - Motivação:
                - Criar um professor sem informar nome
            - Regra de negócio:
                - O usuário que informar e-mail e senha corretamente,
                receberá o token de acesso da aplicação.
            - Resultado Esperado:
                - status: 400
        """

        url = '/professores/'
        data = {
            'email': 'novo_professor@teste.com',
            'senha':'teste'
        }
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_cadastrar_professor_sem_email(self):
        """
            - Motivação:
                - Criar um professor sem informar e-mail
            - Regra de negócio:
                - O usuário que informar e-mail e senha corretamente,
                receberá o token de acesso da aplicação.
            - Resultado Esperado:
                - status: 400
        """

        url = '/professores/'
        data = {
            'nome': 'Professor Teste 2',
            'senha':'teste'
        }
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_cadastrar_professor_email_cadastrado(self):
        """
            - Motivação:
                - Criar um professor com e-mail de outro usuário.
            - Regra de negócio:
                - O usuário que informar e-mail e senha corretamente,
                receberá o token de acesso da aplicação.
            - Resultado Esperado:
                - status: 400
        """

        url = '/professores/'
        data = {
            'nome': 'Professor Teste 2',
            'email': self.professor.email,
            'senha':'teste'
        }
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_professor_alterar_nome(self):
        """
            - Motivação:
                - Alterar o nome do professor.
            - Regra de negócio:
                - Deve ser informado o nome do professor
                para alterar.
            - Resultado Esperado:
                - status: 200
        """

        url = f'/professores/{self.professor.codigo}/'
        data = {
            'nome': 'Professor Teste 2',
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.professor.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            self.professor.nome,
            response.data['nome'],
        )

    def test_professor_alterar_email(self):

        url = f'/professores/{self.professor.codigo}/'
        data = {
            'email': 'email@teste.com',
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.professor.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            self.professor.email,
            response.data['email']
        )

    def test_professor_alterar_senha(self):
        """
            - Motivação:
                - Alterar a senha do professor
            - Regra de negócio:
                - Para alterar a senha, devem ser informados o campos:
                senha, confirmacao_senha e nova_senha.
                - O conteúdo do campo nova_senha deve ser igual ao do campo
                confirmacao_senha para poder ser alterada.
                - Deve ser informada uma nova senha.
            - Resultado Esperado:
                - status: 200
        """

        url = f'/professores/{self.professor.codigo}/'
        data = {
            'senha': '123',
            'nova_senha': 'teste123',
            'confirmacao_senha': 'teste123'
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.professor.refresh_from_db()

        assert check_password(data['nova_senha'], self.professor.password)

    def test_professor_alterar_senha_sem_confirmacao_senha(self):
        """
            - Motivação:
                - Alterar a senha do professor sem a confirmação
                da senha.
            - Regra de negócio:
                - O conteúdo do campo senha deve ser igual ao do campo
                confirmacao_senha para poder ser alterada.
                - Deve ser informado o campo confirmacao_senha
            - Resultado Esperado:
                - status: 400
        """

        url = f'/professores/{self.professor.codigo}/'
        data = {
            'senha': '123',
            'nova_senha': 'teste123'
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_professor_alterar_senha_sem_nova_senha(self):
        """
            - Motivação:
                - Alterar a senha do professor sem a confirmação
                da senha.
            - Regra de negócio:
                - Deve ser informada uma nova senha.
            - Resultado Esperado:
                - status: 400
        """

        url = f'/professores/{self.professor.codigo}/'
        data = {
            'senha': '123',
            'confirmacao_senha': '123',
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_professor_alterar_senha_incorreta(self):
        """
            - Motivação:
                - Ao alterar a senha do professor, a senha atual é
                passada de forma incorreta.
            - Regra de negócio:
                - A senha informada deve estar correta.
            - Resultado Esperado:
                - status: 400
        """

        url = f'/professores/{self.professor.codigo}/'
        data = {
            'senha': '1234',
            'confirmacao_senha': '123',
            'nova_senha': '123',
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_professor_alterar_senha_diferente_confirmacao(self):
        """
            - Motivação:
                - Ao alterar a senha do professor, a nova senha é
                diferente do que está no campo confirmacao_senha
            - Regra de negócio:
                - O conteúdo do campo nova_senha deve ser o mesmo do
                confirmacao_senha
            - Resultado Esperado:
                - status: 400
        """

        url = f'/professores/{self.professor.codigo}/'
        data = {
            'senha': '123',
            'nova_senha': '123r',
            'confirmacao_senha': '12345'
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_remover_professor(self):

        professor = Professor.objects.create(
            nome='Professor Deletado',
            email='professor_delete@teste.com',
            password='123'
        )

        url = f'/professores/{professor.codigo}/'
        response = self.client.delete(
            url
        )

        tem_professor = Professor.objects.filter(
            email='professor_delete@teste.com'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(tem_professor)

    def test_listar_professores(self):
        """
            - Motivação:
                - Listar professores cadastrados.
            - Regra de negócio:
                - Todos os professores cadastrados são listados com
                nome, e-mail e código
            - Resultado Esperado:
                - status: 200
                - paginação
        """

        url = f'/professores/'
        response = self.client.get(
            url
        )

        quantidade = Professor.objects.count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        assert response.data['quantidade'] == quantidade

        assert all(
            key_response in self.pagination_keys for key_response in response.data.keys()
        )



