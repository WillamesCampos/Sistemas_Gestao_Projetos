from datetime import datetime, timedelta

from rest_framework import status
from apps.projetos.models import GrupoTarefa, Tarefa
from apps.usuarios.tests.factory.usuarios import AlunoFactory

from apps.usuarios.tests.test_login import TestCore
from apps.turmas.tests.factory.turmas import (
    TurmaAlunoFactory, TurmaFactory,
    DisciplinaFactory
)
from apps.projetos.tests.factory.projetos import (
    GrupoFactory, GrupoTarefaFactory,
    ProjetoFactory, TarefaFactory
)


class TestTarefaProfessor(TestCore):

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

        cls.disciplina = DisciplinaFactory(
            professor=cls.professor,
            quantidade_grupos=3
        )

        cls.projeto = ProjetoFactory(
            professor=cls.professor,
            disciplina=cls.disciplina
        )

        cls.integrante_grupo = AlunoFactory()
        cls.grupo = GrupoFactory(
            lider=cls.aluno,
            aluno=cls.integrante_grupo
        )

    def test_listar_tarefas(self):

        tarefa = TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        GrupoTarefaFactory(
            grupo=self.grupo,
            tarefa=tarefa
        )

        url = '/tarefas/'
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['resultados'][0]['codigo'],
            tarefa.codigo
        )

    def test_filtrar_tarefa_nome(self):

        tarefa = TarefaFactory(
            nome='Teste',
            projeto=self.projeto,
            responsavel=self.aluno
        )

        TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        GrupoTarefaFactory(
            grupo=self.grupo,
            tarefa=tarefa
        )

        numero_tarefas = Tarefa.objects.filter(
            projeto=self.projeto
        ).count()

        url = '/tarefas/?nome=Teste'
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['resultados'][0]['codigo'],
            tarefa.codigo
        )
        self.assertEqual(
            response.data['quantidade'],
            numero_tarefas
        )

    def test_filtrar_tarefa_situacao(self):

        tarefa = TarefaFactory(
            situacao='concluida',
            projeto=self.projeto,
            responsavel=self.aluno
        )

        TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        GrupoTarefaFactory(
            grupo=self.grupo,
            tarefa=tarefa
        )

        numero_tarefas = Tarefa.objects.filter(
            situacao='concluida'
        ).count()

        url = '/tarefas/?situacao=concluida'
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['resultados'][0]['codigo'],
            tarefa.codigo
        )
        self.assertEqual(
            response.data['quantidade'],
            numero_tarefas
        )

    def test_filtrar_tarefa_disciplina(self):

        tarefa = TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        disciplina = DisciplinaFactory(
            nome='Teste',
            professor=self.professor
        )

        projeto = ProjetoFactory(
            disciplina=disciplina,
            professor=self.professor
        )

        TarefaFactory(
            projeto=projeto,
            responsavel=self.aluno
        )

        GrupoTarefaFactory(
            grupo=self.grupo,
            tarefa=tarefa
        )

        numero_tarefas = Tarefa.objects.filter(
            projeto__disciplina__nome=self.disciplina.nome
        ).count()

        url = f'/tarefas/?disciplina={self.disciplina.nome}'
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['resultados'][0]['codigo'],
            tarefa.codigo
        )
        self.assertEqual(
            response.data['quantidade'],
            numero_tarefas
        )

    def test_criar_tarefa(self):

        url = '/tarefas/'
        data = {
            'projeto': str(self.projeto.codigo),
            'nome': 'Uma tarefa',
            'descricao': 'Uma descricao',
            'data': datetime.now().strftime(
                "%d/%m/%Y"
            ),
            'hora': datetime.now().strftime(
                "%H:%M:%S"
            )
        }

        response = self.client.post(
            url, data=data
        )

        tarefa = Tarefa.objects.get(nome=data['nome'])

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data['nome'],
            tarefa.nome
        )

    def test_editar_tarefa(self):

        tarefa = TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        url = f'/tarefas/{str(tarefa.codigo)}/'
        data = {
            'nome': 'Uma tarefa Dois',
            'descricao': 'Uma descricao Dois',
            'data': (datetime.now() + timedelta(days=3)).strftime(
                "%d/%m/%Y"
            ),
            'hora': (datetime.now() + timedelta(hour=1)).strftime(
                "%H:%M:%S"
            )
        }

        response = self.client.patch(
            url, data=data
        )

        tarefa.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['nome'],
            tarefa.nome
        )
        self.assertEqual(
            response.data['descricao'],
            tarefa.descricao
        )

    
