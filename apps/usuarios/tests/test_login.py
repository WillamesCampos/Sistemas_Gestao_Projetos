from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.usuarios.models import Professor, Aluno


class TestCore(APITestCase):

    """
        Classe base para testes.
        - O usuário aluno já está autenticado.
        - Para autenticar o professor na rota, deve-se
        acessar a rota de login com as credenciais do professor
        e armazenar o seu token de acesso.
    """

    def setUp(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=self.token
        )

    @classmethod
    def setUpTestData(cls) -> None:

        cls.pagination_keys = [
            'pagina_atual',
            'links',
            'quantidade',
            'resultados'
        ]

        cls.professor = Professor.objects.create(
            nome="Professor Teste",
            email="professor@teste.com",
            password=make_password("123")
        )

        cls.aluno = Aluno.objects.create(
            nome="Aluno Teste",
            email="aluno@teste.com",
            password=make_password("123"),
            matricula='20220000000'
        )

        cls.client = APIClient()
        response = cls.client.post(
            '/login/',
            data={
                'username': cls.aluno.email,
                'password': '123'
            }
        )

        cls.token = f'Token {response.data.get("token")}'
        cls.client.credentials(
            HTTP_AUTHORIZATION=cls.token
        )


class TestAutenticacaoUsuario(TestCore):
    """
        Conjuto de testes que verifica as rotas de login
        e recuperação de acesso.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_login_aluno_sucesso(self):
        """
            - Motivação:
                - Testar rota de login com um usuário aluno.
            - Regra de negócio:
                - O usuário que informar e-mail e senha corretamente,
                receberá o token de acesso da aplicação.
            - Resultado Esperado:
                - status: 200
                - retornado token de acesso
        """

        self.client.logout()

        response = self.client.post(
            '/login/',
            data={
                'username': self.aluno.email,
                'password': "123"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        assert response.data.get('token')

    def test_login_professor_sucesso(self):
        """
            - Motivação:
                - Testar rota de login com um usuário professor.
            - Regra de negócio:
                - O usuário que informar e-mail e senha corretamente,
                receberá o token de acesso da aplicação.
            - Resultado Esperado:
                - status: 200
                - retornado token de acesso
        """

        self.client.logout()

        response = self.client.post(
            '/login/',
            data={
                'username': self.professor.email,
                'password': "123"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        assert response.data.get('token')

    def test_login_falha_autenticacao(self):
        """
            - Motivação:
                - Testar rota de login com um usuário,
                informando senha errada.
            - Regra de negócio:
                - O usuário não terá acesso se informar
                e-mail e senha diferente do que foi cadastrado
                e não será autenticado.
            - Resultado Esperado:
                - status: 400
        """

        self.client.logout()

        response = self.client.post(
            '/login/',
            data={
                'username': self.aluno.email,
                'password': "1234"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        assert 'token' not in response.data.keys()

    def test_login_sem_informar_email(self):
        """
            - Motivação:
                - Testar rota de login com um usuário sem informar
                o e-mail..
            - Regra de negócio:
                - Não tem como ser autenticado sem informar e-mail.
            - Resultado Esperado:
                - status: 400
        """

        self.client.logout()

        response = self.client.post(
            '/login/',
            data={
                'password': "123"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        assert 'token' not in response.data.keys()

    def test_login_sem_informar_senha(self):
        """
            - Motivação:
                - Testar rota de login com um usuário sem informar
                a senha.
            - Regra de negócio:
                - Não tem como ser autenticado sem informar senha.
            - Resultado Esperado:
                - status: 400
        """

        self.client.logout()

        response = self.client.post(
            '/login/',
            data={
                'username': self.aluno.email
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        assert 'token' not in response.data.keys()

    def test_recuperar_acesso_senha(self):
        """
            - Motivação:
                - Rota para gerar uma nova senha.
            - Regra de negócio:
                - O usuário que informar e-mail válido que
                pertence a um usuário cadastrado e
                informar uma senha nova.
            - Resultado Esperado:
                - status: 200
                - retornado token de acesso
        """
        self.client.logout()

        url = '/recuperar-acesso/senha/'
        data = {
                "email": self.aluno.email,
                "nova_senha": "1234"
            }

        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_recuperar_acesso_senha_email_sem_usuario(self):
        """
            - Motivação:
                - Rota para gerar uma nova senha.
            - Regra de negócio:
                - O e-mail informado deve pertencer a um
                usuário cadastrado.
            - Resultado Esperado:
                - status: 400
        """
        self.client.logout()

        url = '/recuperar-acesso/senha/'
        data = {
                "email": "email@teste.com",
                "nova_senha": "1234"
            }

        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
