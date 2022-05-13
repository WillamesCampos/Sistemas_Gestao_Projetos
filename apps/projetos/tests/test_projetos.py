from rest_framework import status
from apps.usuarios.tests.factory.usuarios import ProfessorFactory
from apps.usuarios.tests.test_login import TestCore
from apps.projetos.tests.factory.projetos import (
    GrupoFactory, ProjetoFactory, ProjetoGrupoFactory
)
from apps.turmas.tests.factory.turmas import DisciplinaFactory
from apps.projetos.models import Projeto, ProjetoGrupo

from factory import Faker


class TestProjeto(TestCore):

    """
        Testes para manutenir projetos e gerenciar grupos
        no projeto.
        - Funcionalidades exclusivas para o professor.
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

        cls.disciplina = DisciplinaFactory(
            professor=cls.professor,
            quantidade_grupos=3
        )

    def test_criar_projeto(self):
        """
            - Motivação:
                - Criar um projeto
            - Regra de negócio:
                - Apenas um professor pode criar um projeto.
                - Informar uma disciplina que o professor leciona.
            - Resultado Esperado:
                - status: 201
        """

        url = '/projetos/'
        data = {
            'nome': 'Projeto de cobertura de Testes',
            'tipo': 'Testes',
            'area': 'Testes Unitários',
            'descricao': 'Lorem Ipsum',
            'disciplina': f'{self.disciplina.codigo}'
        }

        response = self.client.post(
            url, data=data
        )

        projeto = Projeto.objects.get(nome=data['nome'])

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.data['codigo'],
            projeto.codigo
        )
        self.assertEqual(
            response.data['professor']['codigo'],
            self.professor.codigo
        )
        self.assertEqual(
            response.data['disciplina']['codigo'],
            self.disciplina.codigo
        )

    def test_criar_projeto_sem_disciplina_professor(self):
        """
            - Motivação:
                - Criar um projeto com uma disciplina que o
                professor não leciona.
            - Regra de negócio:
                - Apenas um professor pode criar um projeto.
                - Informar uma disciplina que o professor leciona.
            - Resultado Esperado:
                - status: 400
        """
        professor = ProfessorFactory()

        disciplina = DisciplinaFactory(
            professor=professor
        )

        url = '/projetos/'
        data = {
            'nome': 'Projeto de cobertura de Testes',
            'tipo': 'Testes',
            'area': 'Testes Unitários',
            'descricao': 'Lorem Ipsum',
            'disciplina': f'{disciplina.codigo}'
        }

        response = self.client.post(
            url, data=data
        )
        projeto = Projeto.objects.filter(nome=data['descricao'])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertFalse(projeto)
        self.assertEqual(
            str(response.data['disciplina'][0]),
            'A disciplina informada não pertence ao professor.'
        )

    def test_criar_projeto_sem_nome(self):
        """
            - Motivação:
                - Criar um projeto sem nome
            - Regra de negócio:
                - Não é possível criar projeto sem nome.
            - Resultado Esperado:
                - status: 400
        """

        url = '/projetos/'
        data = {
            'tipo': 'Testes',
            'area': 'Testes Unitários',
            'descricao': 'Lorem Ipsum',
            'disciplina': f'{self.disciplina.codigo}'
        }

        response = self.client.post(
            url, data=data
        )

        projeto = Projeto.objects.filter(nome=data['descricao'])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertFalse(projeto)
        self.assertEqual(
            str(response.data['nome'][0]),
            'Este campo é obrigatório.'
        )

    def test_criar_projeto_sem_tipo(self):
        """
            - Motivação:
                - Criar um projeto sem tipo
            - Regra de negócio:
                - Não é possível criar projeto sem tipo.
            - Resultado Esperado:
                - status: 400
        """

        url = '/projetos/'
        data = {
            'nome': Faker('company', locale='pt_BR'),
            'area': 'Testes Unitários',
            'descricao': 'Lorem Ipsum',
            'disciplina': f'{self.disciplina.codigo}'
        }

        response = self.client.post(
            url, data=data
        )

        projeto = Projeto.objects.filter(nome=data['nome'])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertFalse(projeto)
        self.assertEqual(
            str(response.data['tipo'][0]),
            'Este campo é obrigatório.'
        )

    def test_criar_projeto_sem_area(self):
        """
            - Motivação:
                - Criar um projeto sem área
            - Regra de negócio:
                - Não é possível criar projeto sem área.
            - Resultado Esperado:
                - status: 400
        """

        url = '/projetos/'
        data = {
            'nome': Faker('company', locale='pt_BR'),
            'tipo': 'Testes',
            'descricao': 'Lorem Ipsum',
            'disciplina': f'{self.disciplina.codigo}'
        }

        response = self.client.post(
            url, data=data
        )

        projeto = Projeto.objects.filter(nome=data['nome'])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertFalse(projeto)
        self.assertEqual(
            str(response.data['area'][0]),
            'Este campo é obrigatório.'
        )

    def test_listar_projetos(self):
        """
            - Motivação:
                - Lista os projetos cadastrados.
            - Regra de negócio:
                - Lista os projetos com os grupos
                associados, se tiver.
                - Lista apenas os projetos criados
                pelo professor.
            - Resultado Esperado:
                - status: 200
        """

        projetos = ProjetoFactory.create_batch(
            size=5,
            professor=self.professor,
            disciplina=self.disciplina
        )

        grupos = GrupoFactory.create_batch(size=5)

        for projeto, grupo in zip(projetos, grupos):
            ProjetoGrupoFactory(
                projeto=projeto,
                grupo=grupo
            )

        url = '/projetos/'

        response = self.client.get(
            url
        )

        total_projetos = Projeto.objects.filter(
            professor=self.professor
        ).count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['quantidade'],
            total_projetos
        )

    def test_editar_nome_projeto(self):
        """
            - Motivação:
                - Editar nome de um projeto
                associado ao professor.
            - Regra de negócio:
                - Apenas projetos associados ao
                professor podem ser alterados.
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        url = f'/projetos/{projeto.codigo}/'
        data = {
            'nome': 'Projeto mudou de nome'
        }

        response = self.client.patch(
            url,
            data=data
        )

        projeto.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            projeto.nome,
            response.data['nome']
        )
        self.assertEqual(
            response.data['codigo'],
            projeto.codigo
        )

    def test_editar_tipo_projeto(self):
        """
            - Motivação:
                - Editar tipo de um projeto
                associado ao professor.
            - Regra de negócio:
                - Apenas projetos associados ao
                professor podem ser alterados.
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        url = f'/projetos/{projeto.codigo}/'
        data = {
            'tipo': 'Tipo alterado'
        }

        response = self.client.patch(
            url,
            data=data
        )

        projeto.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            projeto.tipo,
            response.data['tipo']
        )
        self.assertEqual(
            response.data['codigo'],
            projeto.codigo
        )

    def test_editar_area_projeto(self):
        """
            - Motivação:
                - Editar área de um projeto
                associado ao professor.
            - Regra de negócio:
                - Apenas projetos associados ao
                professor podem ser alterados.
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        url = f'/projetos/{projeto.codigo}/'
        data = {
            'tipo': 'Area alterada'
        }

        response = self.client.patch(
            url,
            data=data
        )

        projeto.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            projeto.area,
            response.data['area']
        )
        self.assertEqual(
            response.data['codigo'],
            projeto.codigo
        )

    def test_vincular_grupo_em_projeto_nao_consolidado(self):
        """
            - Motivação:
                - Associar grupos a um projeto.
            - Regra de negócio:
                - Apenas projetos associados ao
                professor podem ter grupos vinculados.
                - O projeto deve estar ativo para ser
                gerenciado
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        grupo = GrupoFactory()

        url = f'/projetos/{projeto.codigo}/gerenciar-grupos/'
        data = {
            'grupo': f'{grupo.codigo}'
        }

        response = self.client.patch(
            url,
            data=data
        )

        projeto.refresh_from_db()

        projeto_grupo = ProjetoGrupo.objects.filter(
            projeto=projeto,
            grupo=grupo
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        assert projeto_grupo
        self.assertEqual(
            projeto_grupo[0].grupo.codigo,
            response.data['grupos'][0]['codigo']
        )

    def test_vincular_mesmo_grupo_mesmo_projeto(self):
        """
            - Motivação:
                - Associar grupos a um projeto.
            - Regras de negócio:
                - Apenas projetos associados ao
                professor podem ter grupos vinculados;
                - O projeto deve estar ativo para ser
                gerenciado;
                - Um grupo não pode ser vinculado
                2 vezes ao mesmo projeto.
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina,
        )

        grupo = GrupoFactory()

        ProjetoGrupoFactory(
            projeto=projeto,
            grupo=grupo
        )

        url = f'/projetos/{projeto.codigo}/gerenciar-grupos/'
        data = {
            'grupo': f'{grupo.codigo}'
        }

        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            str(response.data['grupo'][0]),
            'O grupo já está no projeto.'
        )

    def test_vincular_grupo_projeto_consolidado(self):
        """
            - Motivação:
                - Associar grupos a um projeto.
            - Regras de negócio:
                - Apenas projetos associados ao
                professor podem ter grupos vinculados;
                - O projeto deve estar ativo para ser
                gerenciado;
                - Um grupo não pode ser vinculado
                a um projeto já consolidado.
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina,
            consolidado=True
        )

        grupo = GrupoFactory()

        grupo_extra = GrupoFactory()

        ProjetoGrupoFactory(
            projeto=projeto,
            grupo=grupo
        )

        url = f'/projetos/{projeto.codigo}/gerenciar-grupos/'
        data = {
            'grupo': f'{grupo_extra.codigo}'
        }

        response = self.client.patch(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            str(response.data['grupo'][0]),
            'Torne o projeto não consolidado para vincular grupos.'
        )

    def test_vincular_grupo_em_projeto_inativo(self):
        """
            - Motivação:
                - Associar grupos a um projeto.
            - Regras de negócio:
                - Apenas projetos associados ao
                professor podem ter grupos vinculados;
                - O projeto deve estar ativo para ser
                gerenciado;
                - Um grupo não pode ser vinculado
                a um projeto inativo
            - Resultado Esperado:
                - status: 400
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina,
            ativo=False
        )

        grupo = GrupoFactory()

        url = f'/projetos/{projeto.codigo}/gerenciar-grupos/'
        data = {
            'grupo': f'{grupo.codigo}'
        }

        response = self.client.patch(
            url,
            data=data
        )

        projeto_grupo = ProjetoGrupo.objects.filter(
            projeto=projeto,
            grupo=grupo
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        assert not projeto_grupo
        self.assertEqual(
            str(response.data['ativo'][0]),
            'Um projeto deve estar ativo para ser gerenciado.'
        )

    def test_desvincular_grupo_em_projeto_nao_consolidado(self):
        """
            - Motivação:
                - Retira grupos de um projeto.
            - Regra de negócio:
                - Apenas projetos associados ao
                professor podem ter grupos vinculados.
                - O projeto deve estar ativo para ser
                gerenciado
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        grupos = GrupoFactory.create_batch(size=10)

        for grupo in grupos:

            ProjetoGrupoFactory(
                projeto=projeto,
                grupo=grupo
            )

        grupo_removido = grupos[0].codigo

        url = f'/projetos/{projeto.codigo}/gerenciar-grupos/'
        data = {
            'grupos_removidos': f'{grupos[0].codigo}'
        }

        response = self.client.patch(
            url,
            data=data
        )

        projeto.refresh_from_db()

        projeto_grupo = ProjetoGrupo.objects.filter(
            projeto=projeto,
            grupo=grupo_removido
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        assert not projeto_grupo

    def test_consolidar_projeto(self):
        """
            - Motivação:
                - Validar um projeto vinculado a grupo.
            - Regras de negócio:
                - Apenas projetos associados ao
                professor podem ter grupos vinculados;
                - O projeto deve estar ativo para ser
                gerenciado;
                - Para ser consolidado, o projeto deve ter
                apenas 1 grupo.
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        grupo = GrupoFactory()

        ProjetoGrupoFactory(
            projeto=projeto,
            grupo=grupo
        )

        url = f'/projetos/{projeto.codigo}/gerenciar-grupos/'
        data = {
            'consolidado': True
        }

        response = self.client.patch(
            url,
            data=data
        )

        projeto.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        assert projeto.consolidado

    def test_ativar_projeto(self):
        """
            - Motivação:
                - Ativar um projeto.
            - Regras de negócio:
                - Apenas projetos associados ao
                professor podem ser ativados.
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina,
            ativo=False
        )

        grupo = GrupoFactory()

        ProjetoGrupoFactory(
            projeto=projeto,
            grupo=grupo
        )

        url = f'/projetos/{projeto.codigo}/'
        data = {
            'ativo': True
        }

        response = self.client.patch(
            url, data
        )

        projeto.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['ativo'],
            projeto.ativo
        )

    def test_desativar_projeto(self):
        """
            - Motivação:
                - Desativar um projeto.
            - Regras de negócio:
                - Apenas projetos associados ao
                professor podem ser desativados.
            - Resultado Esperado:
                - status: 200
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        grupo = GrupoFactory()

        ProjetoGrupoFactory(
            projeto=projeto,
            grupo=grupo
        )

        url = f'/projetos/{projeto.codigo}/'
        data = {
            'ativo': False
        }

        response = self.client.patch(
            url, data
        )

        projeto.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['ativo'],
            projeto.ativo
        )

    def test_apagar_projeto(self):
        """
            - Motivação:
                - Desativar um projeto.
            - Regras de negócio:
                - Apenas projetos associados ao
                professor podem ser desativados.
                - Os grupos são desassociados.
            - Resultado Esperado:
                - status: 204
        """

        projeto = ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina,
        )

        grupo = GrupoFactory()

        ProjetoGrupoFactory(
            projeto=projeto,
            grupo=grupo
        )

        url = f'/projetos/{projeto.codigo}/'
        response = self.client.delete(
            url
        )

        projeto.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(projeto.ativo)


class TestProjetoAluno(TestCore):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        cls.disciplina = DisciplinaFactory(
            professor=cls.professor,
            quantidade_grupos=3
        )

    def test_filtrar_projetos_professor(self):
        """
            - Motivação:
                - Lista os projetos associados a um professor.
            - Regra de negócio:
                - Lista os projetos com os grupos
                associados, se tiver.
                - Lista apenas os projetos criados
                pelo professor informado no query parameters
            - Resultado Esperado:
                - status: 200
        """

        ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        professor = ProfessorFactory()
        disciplina = DisciplinaFactory(
            professor=professor
        )

        ProjetoFactory(
            professor=professor,
            disciplina=disciplina
        )

        url = f'/projetos/?professor={self.professor.codigo}'

        response = self.client.get(
            url
        )

        total_projetos = Projeto.objects.filter(
            professor=self.professor
        ).count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['quantidade'],
            total_projetos
        )

    def test_filtrar_projetos_ativo(self):
        """
            - Motivação:
                - Lista os projetos associados a um professor.
            - Regra de negócio:
                - Lista os projetos com os grupos
                associados, se tiver.
                - Lista apenas os projetos criados
                pelo professor informado no query parameters
            - Resultado Esperado:
                - status: 200
        """

        ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        professor = ProfessorFactory()
        disciplina = DisciplinaFactory(
            professor=professor
        )

        ProjetoFactory(
            professor=professor,
            disciplina=disciplina,
            ativo=False
        )

        url = '/projetos/?ativo=true'

        response = self.client.get(
            url
        )

        total_projetos = Projeto.objects.filter(
            professor=self.professor
        ).count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['quantidade'],
            total_projetos
        )

    def test_filtrar_projetos_disciplina(self):
        """
            - Motivação:
                - Lista os projetos associados a uma disciplina.
            - Regra de negócio:
                - Lista os projetos com os grupos
                associados, se tiver.
                - Lista apenas os projetos associados a uma
                disciplina no query parameters.
            - Resultado Esperado:
                - status: 200
        """

        ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        professor = ProfessorFactory()
        disciplina = DisciplinaFactory(
            professor=professor
        )

        ProjetoFactory(
            professor=professor,
            disciplina=disciplina,
            ativo=False
        )

        url = f'/projetos/?disciplina={self.disciplina.codigo}'

        response = self.client.get(
            url
        )

        total_projetos = Projeto.objects.filter(
            professor=self.professor
        ).count()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['quantidade'],
            total_projetos
        )
