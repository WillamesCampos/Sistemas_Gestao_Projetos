from datetime import datetime, timedelta

from rest_framework import status
from apps.projetos.models import Tarefa
from apps.usuarios.tests.factory.usuarios import AlunoFactory, ProfessorFactory

from apps.usuarios.tests.test_login import TestCore
from apps.turmas.tests.factory.turmas import (
    DisciplinaFactory
)
from apps.projetos.tests.factory.projetos import (
    GrupoFactory, GrupoTarefaFactory,
    ProjetoFactory, ProjetoGrupoFactory, TarefaFactory
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
        """
            - Motivação:
                - Listar as tarefas do projeto da disciplina
                que o professor leciona.
            - Regra de negócio:
                - Todas as tarefas dos projetos do professor são
                exibidos.
            - Resultado Esperado:
                - status: 200
                - paginação
        """

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
        """
            - Motivação:
                - Filtrar tarefas pelo nome
            - Regra de negócio:
                - São exibidas apenas as tarefas com os caracteres que
                estão no nome da tarefa, informados no query parameters "nome"
            - Resultado Esperado:
                - status: 200
                - paginação
        """

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
        """
            - Motivação:
                - Filtrar tarefas pela situação
            - Regra de negócio:
                - São exibidas apenas as tarefas com a situação informada
                no query parameters no campo "situacao".
            - Resultado Esperado:
                - status: 200
                - paginação
        """

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

    def test_filtrar_tarefa_nome_disciplina(self):
        """
            - Motivação:
                - Filtrar tarefas pelo nome da disciplina
            - Regra de negócio:
                - São exibidas apenas as tarefas com o nome da
                disciplina informada no query parameters no
                campo "disciplina".
            - Resultado Esperado:
                - status: 200
                - paginação
        """

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

    def test_filtrar_tarefa_nome_professor(self):
        """
            - Motivação:
                - Filtrar tarefas pelo nome do professor
            - Regra de negócio:
                - São exibidas as tarefas com o nome do professor informado
                no query parameters no campo "professor".
            - Resultado Esperado:
                - status: 200
                - paginação
        """

        tarefa = TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        professor = ProfessorFactory(
            nome='Outro Professor'
        )

        disciplina = DisciplinaFactory(
            nome='Teste',
            professor=professor
        )

        aluno = AlunoFactory()

        projeto = ProjetoFactory(
            disciplina=disciplina,
            professor=professor
        )

        TarefaFactory(
            projeto=projeto,
            responsavel=aluno
        )

        numero_tarefas = Tarefa.objects.filter(
            projeto__professor__nome__icontains=self.professor.nome
        ).count()

        url = f'/tarefas/?professor={self.professor.nome}'
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

    def test_filtrar_tarefa_ativa(self):
        """
            - Motivação:
                - Filtrar tarefas ativas
            - Regra de negócio:
                - São exibidas apenas as tarefas com status ativo
                no query parameters no campo "ativo".
            - Resultado Esperado:
                - status: 200
                - paginação
        """

        tarefa = TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        TarefaFactory(
            ativo=False,
            projeto=self.projeto
        )

        numero_tarefas = Tarefa.objects.filter(
            ativo=True
        ).count()

        url = '/tarefas/?ativo=true'
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

    def test_criar_tarefa_projeto_nao_selecionado(self):
        """
            - Motivação:
                - Cria tarefa para um projeto que não foi escolhido
                por nenhum grupo.
            - Regra de negócio:
                - Cria uma única tarefa relacionada ao projeto.
            - Resultado Esperado:
                - status: 201
        """

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

    def test_criar_tarefa_projeto_selecionado(self):
        """
            - Motivação:
                - Cria várias instâncias de tarefas para cada
                grupo associado ao projeto.
            - Regra de negócio:
                - Se um projeto foi selecionado por 1 ou mais grupos:
                A mesma tarefa é enviada para cada grupo, pois o projeto
                é o mesmo.
            - Resultado Esperado:
                - status: 201
        """

        ProjetoGrupoFactory(
            projeto=self.projeto,
            grupo=self.grupo
        )

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
        """
            - Motivação:
                - Edita uma tarefa.
            - Regra de negócio:
                - Altera parâmetros da tarefa.
                - Data e hora, nome e descrição
                são parâmetros que podem ser alterados.
            - Resultado Esperado:
                - status: 200
        """

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
            'hora': (datetime.now() + timedelta(minutes=60)).strftime(
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

    def test_alterar_projeto_tarefa(self):
        """
            - Motivação:
                - Altera um projeto de uma tarefa.
            - Regra de negócio:
                - Todas as tarefas que forem designadas
                a diferentes grupos, mas com mesmo conteúdo,
                também têm o projeto mudado.
            - Resultado Esperado:
                - status: 200
        """

        tarefa = TarefaFactory(
            projeto=self.projeto,
            nome='Teste'
        )

        projeto = ProjetoFactory(
            professor=self.professor,
            nome='Projeto Extra',
            disciplina=self.disciplina
        )

        url = f'/tarefas/{tarefa.codigo}/'
        data = {
            'projeto': str(projeto.codigo)
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
            response.data['projeto']['codigo'],
            tarefa.projeto.codigo
        )

    def test_desativar_tarefa(self):
        """
            - Motivação:
                - Desativar uma tarefa
            - Regra de negócio:
                - A tarefa fica com status ativo = False
                e situação cancelada.
            - Resultado Esperado:
                - status: 204
        """

        tarefa = TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        url = f'/tarefas/{tarefa.codigo}/'

        response = self.client.delete(
            url
        )

        tarefa.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            tarefa.situacao,
            'cancelada'
        )
        self.assertFalse(tarefa.ativo)


class TestTarefaAluno(TestCore):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

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

    def test_visualizar_tarefas_grupo(self):
        """
            - Motivação:
                - Exibir tarefas do usuário que pertence a um grupo
            - Regra de negócio:
                - São listadas as tarefas associadas ao grupo que o
                aluno logado é líder ou membro.
            - Resultado Esperado:
                - status: 200
        """

        tarefa = TarefaFactory(
            projeto=self.projeto,
            responsavel=self.aluno
        )

        GrupoTarefaFactory(
            grupo=self.grupo,
            tarefa=tarefa
        )

        url = f'/tarefas/{tarefa.codigo}/visualizar/'

        response = self.client.get(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
