from uuid import uuid4
from datetime import datetime
from random import choice

from rest_framework import status
from apps.usuarios.tests.test_login import TestCore
from apps.turmas.tests.factory.turmas import TurmaFactory
from apps.usuarios.tests.factory.usuarios import AlunoFactory
from apps.turmas.models import Turma
from apps.usuarios.models import Aluno


class TestTurmasAluno(TestCore):

    """
        Testes para acessar turmas.
        - Já tem um aluno logado.
        - Já existe uma turma cadastrada e associada ao
        aluno.
    """
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.turma = TurmaFactory()

        cls.aluno.turma = cls.turma
        cls.aluno.save()

    def test_listar_turmas_aluno(self):
        """
            - Motivação:
                - Listar todas as turmas cadastradas.
            - Regra de negócio:
                - O aluno só acessa a turma que foi
                cadastrado.
            - Resultado Esperado:
                - status: 200
        """

        url = '/turmas/'
        response = self.client.get(url)

        total_turmas_aluno = Turma.objects.filter(aluno=self.aluno).count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        assert all(
            key_response in self.pagination_keys for key_response in response.data.keys() # noqa
        )

        self.assertEqual(
            response.data['quantidade'],
            total_turmas_aluno
        )

        self.assertEqual(
            response.data['resultados'][0]['codigo'],
            str(self.turma.codigo)
        )

    def test_turma_inserir_alunos(self):
        """
            - Motivação:
                - Inserir alunos na turma
            - Regra de negócio:
                -Apenas professores podem inserir alunos
                na turma.
            - Resultado Esperado:
                - status: 403
        """

        alunos = AlunoFactory.create_batch(size=5)

        data = {
            'alunos': [str(aluno.codigo) for aluno in alunos]
        }

        url = f'/turmas/{self.turma.codigo}/adicionar-alunos/'
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            str(response.data['detail']),
            'Você não tem permissão para executar essa ação.'
        )

    def test_criar_turma(self):
        """
            - Motivação:
                - Criar turma com usuário aluno logado.
            - Regra de negócio:
                - Somente professores podem manutenir
                turmas.
            - Resultado Esperado:
                - status: 403
        """

        url = '/turmas/'
        data = {
            'nome': 'Turma do Barulho',
            'periodo': datetime.now().strftime('%Y') + str(choice(range(1, 3))) # noqa
        }
        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            str(response.data['detail']),
            'Você não tem permissão para executar essa ação.'
        )

    def test_editar_nome_turma(self):
        """
            - Motivação:
                - Editar o nome da turma, com o
                usuário aluno logado.
            - Regra de negócio:
                - Apenas o professor pode manutenir
                turmas.
            - Resultado Esperado:
                - status: 403
        """

        url = f'/turmas/{self.turma}/'
        data = {
            'nome': 'KND a Turma do Bairro',
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.turma.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            str(response.data['detail']),
            'Você não tem permissão para executar essa ação.'
        )

    def test_turma_remover_alunos(self):
        """
            - Motivação:
                - Remover alunos da turma.
            - Regra de negócio:
                - Apenas o professor pode remover alunos
                da turma.
            - Resultado Esperado:
                - status: 403
        """

        url = f'/turmas/{self.turma.codigo}/remover-alunos/'
        response = self.client.patch(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            str(response.data['detail']),
            'Você não tem permissão para executar essa ação.'
        )

    def test_apagar_turma(self):
        """
            - Motivação:
                - Apagar uma turma.
            - Regra de negócio:
                - Apenas o professor pode apagar uma turma.
            - Resultado Esperado:
                - status: 403
        """

        turma = TurmaFactory()
        self.aluno.turma = turma
        self.aluno.save()

        url = f'/turmas/{turma}/'
        response = self.client.delete(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            str(response.data['detail']),
            'Você não tem permissão para executar essa ação.'
        )


class TestTurmasProfessor(TestCore):
    """
        Testes para manutenir turmas logado com o usuário
        professor.
        - Já tem um professor logado
        - Já existe uma turma cadastrada e associada ao
        professor.
    """

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

        cls.turma = TurmaFactory()
        cls.professor.turma = cls.turma

        cls.professor.save()

    def test_listar_turmas_professor(self):
        """
            - Motivação:
                - Listar todas as turmas cadastradas.
            - Regra de negócio:
                - O professor pode ver todas as turmas.
            - Resultado Esperado:
                - status: 200
        """

        TurmaFactory.create_batch(size=5)

        url = '/turmas/'
        response = self.client.get(url)

        total_turmas = Turma.objects.count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        assert all(
            key_response in self.pagination_keys for key_response in response.data.keys() # noqa
        )

        assert response.data['quantidade'] == total_turmas

    def test_turma_inserir_alunos(self):
        """
            - Motivação:
                - Inserir alunos em uma turma.
            - Regra de negócio:
                - O professor pode inserir 1 ou mais
                alunos em uma turma.
            - Resultado Esperado:
                - status: 200
        """

        alunos = AlunoFactory.create_batch(size=5)

        data = {
            'alunos': [str(aluno.codigo) for aluno in alunos]
        }

        total_alunos_antes_requisitar = Aluno.objects.filter(
            turma=self.turma
        ).count()

        url = f'/turmas/{self.turma.codigo}/adicionar-alunos/'
        response = self.client.patch(
            url,
            data=data
        )

        total_alunos_na_turma = Aluno.objects.filter(
            turma=self.turma
        ).count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        assert all(
            str(aluno['codigo']) in data['alunos'] for aluno in response.data['alunos'] # noqa
        )
        self.assertNotEqual(
            total_alunos_antes_requisitar,
            total_alunos_na_turma
        )

    def test_turma_remover_alunos(self):
        """
            - Motivação:
                - Remover alunos da turma.
            - Regra de negócio:
                - O professor pode remover 1 ou mais
                alunos da turma.
            - Resultado Esperado:
                - status: 200
        """

        alunos = AlunoFactory.create_batch(
            size=5,
            turma=self.turma
        )

        data = {
            'alunos': [str(aluno.codigo) for aluno in alunos]
        }

        total_alunos_antes_requisitar = Aluno.objects.filter(
            turma=self.turma
        ).count()

        url = f'/turmas/{self.turma.codigo}/remover-alunos/'
        response = self.client.patch(
            url,
            data=data
        )

        total_alunos_na_turma = Aluno.objects.filter(
            turma=self.turma
        ).count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertNotEqual(
            total_alunos_antes_requisitar,
            total_alunos_na_turma
        )

        assert not response.data['alunos']

    def test_turma_inserir_nenhum_aluno(self):
        """
            - Motivação:
                - Informar lista de alunos vazia para
                inserir alunos na turma.
            - Regra de negócio:
                - Não é possível inserir alunos, se nenhum
                foi informado (incluindo listas vazias).
            - Resultado Esperado:
                - status: 400
        """

        data = {
            'alunos': []
        }

        url = f'/turmas/{self.turma.codigo}/adicionar-alunos/'
        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            str(response.data['alunos'][0]),
            'Este campo é obrigatório. Deve ser informado pelo menos 1 aluno.' # noqa
        )

    def test_criar_turma(self):
        """
            - Motivação:
                - Criar uma turma.
            - Regra de negócio:
                - O professor deve informar o nome
                e o período da turma para criar.
                alunos da turma.
            - Resultado Esperado:
                - status: 200
        """

        url = '/turmas/'
        data = {
            'nome': 'Turma do Barulho',
            'periodo': datetime.now().strftime('%Y') + str(choice(range(1, 3))) # noqa
        }
        response = self.client.post(
            url,
            data=data
        )

        turma_criada = Turma.objects.get(nome=data['nome'])

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            str(turma_criada.codigo),
            response.data['codigo']
        )

    def test_criar_turma_sem_nome(self):
        """
            - Motivação:
                - Criar uma turma sem informar nome.
            - Regra de negócio:
                - O professor deve informar o nome
                e o período da turma para criar.
                alunos da turma.
            - Resultado Esperado:
                - status: 400
        """

        total_turmas = Turma.objects.count()

        url = '/turmas/'
        data = {
            'periodo': datetime.now().strftime('%Y') + str(choice(range(1, 3))) # noqa
        }
        response = self.client.post(
            url,
            data=data
        )

        total_turmas_apos_requisicao = Turma.objects.count()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            total_turmas,
            total_turmas_apos_requisicao
        )
        self.assertEqual(
            str(response.data['nome'][0]),
            'Este campo é obrigatório.'
        )

    def test_criar_turma_sem_periodo(self):
        """
            - Motivação:
                - Criar uma turma sem informar o
                período.
            - Regra de negócio:
                - O professor deve informar o nome
                e o período da turma para criar.
                alunos da turma.
            - Resultado Esperado:
                - status: 200
        """

        total_turmas = Turma.objects.count()

        url = '/turmas/'
        data = {
            'nome': 'Turma do Barulho',
        }
        response = self.client.post(
            url,
            data=data
        )

        total_turmas_apos_requisicao = Turma.objects.count()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            total_turmas,
            total_turmas_apos_requisicao
        )
        self.assertEqual(
            str(response.data['periodo'][0]),
            'Este campo é obrigatório.'
        )

    def test_editar_nome_turma(self):
        """
            - Motivação:
                - Editar o nome de uma turma.
            - Regra de negócio:
                - O professor deve informar o nome
                para alterar.
                alunos da turma.
            - Resultado Esperado:
                - status: 200
        """

        url = f'/turmas/{self.turma}/'
        data = {
            'nome': 'KND a Turma do Bairro',
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.turma.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            self.turma.nome,
            response.data['nome']
        )

    def test_editar_periodo_turma(self):
        """
            - Motivação:
                - Editar o período de uma turma.
            - Regra de negócio:
                - O professor deve informar o período
                para alterar.
            - Resultado Esperado:
                - status: 200
        """

        url = f'/turmas/{self.turma}/'
        data = {
            'periodo': datetime.now().strftime("%Y") + '.T',
        }
        response = self.client.patch(
            url,
            data=data
        )

        self.turma.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            self.turma.periodo,
            response.data['periodo']
        )

    def test_apagar_turma(self):
        """
            - Motivação:
                - Apagar uma turma.
            - Regra de negócio:
                - Apenas o professor tem permissão
                para apagar uma turma.
            - Resultado Esperado:
                - status: 204
        """

        turma = TurmaFactory()
        codigo_turma = str(turma.codigo)

        url = f'/turmas/{turma}/'
        response = self.client.delete(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Turma.objects.filter(
                codigo=codigo_turma
            )
        )

    def test_apagar_turma_inexistente(self):
        """
            - Motivação:
                - Apagar uma turma, cujo código informado,
                não existe.
            - Regra de negócio:
                - Não é possível apagar uma turma não cadastrada.
            - Resultado Esperado:
                - status: 400
        """

        url = f'/turmas/{str(uuid4())}/'
        response = self.client.delete(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
