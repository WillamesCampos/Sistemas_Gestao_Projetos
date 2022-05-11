from rest_framework import status
from apps.usuarios.tests.factory.usuarios import AlunoFactory

from apps.usuarios.tests.test_login import TestCore
from apps.turmas.tests.factory.turmas import (
    TurmaAlunoFactory, TurmaFactory,
    DisciplinaFactory
)
from apps.projetos.tests.factory.projetos import GrupoFactory, ProjetoFactory
from apps.projetos.models import Grupo


class TestGrupoAluno(TestCore):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        cls.disciplina = DisciplinaFactory(
            professor=cls.professor,
            quantidade_grupos=2
        )

    def test_criar_grupo(self):
        """
            - Motivação:
                - O aluno vai criar o grupo.
            - Regra de negócio:
                - O aluno que cria o grupo automaticamente será o
                líder.
                - O aluno deve pertencer a uma turma da disciplina informada.
            - Resultado Esperado:
                - status: 201
        """

        turma = TurmaFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        TurmaAlunoFactory(
            turma=turma,
            aluno=self.aluno
        )

        url = '/grupos/'

        data = {
            'disciplina': str(self.disciplina.codigo)
        }

        response = self.client.post(
            url, data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        assert response.data['participantes'][0]['lider']

    def test_criar_grupo_sem_participar_turma(self):

        url = '/grupos/'

        response = self.client.post(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            str(response.data['aluno'][0]),
            'Você não pode criar um grupo sem estar em uma turma.'
        )

    def test_filtrar_grupo_disciplina(self):

        turma = TurmaFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        ProjetoFactory(
            professor=self.professor,
            disciplina=self.disciplina
        )

        aluno = AlunoFactory()

        TurmaAlunoFactory(
            turma=turma,
            aluno=self.aluno
        )

        GrupoFactory(
            lider=self.aluno,
            aluno=aluno,
            disciplina=self.disciplina
        )

        disciplina_extra = DisciplinaFactory()

        aluno_extra = AlunoFactory()

        GrupoFactory(
            lider=aluno_extra,
            disciplina=disciplina_extra
        )

        url = f'/grupos/?disciplina={self.disciplina.codigo}'

        response = self.client.get(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        assert response.data[
            'resultados'
        ][0][
            'participantes'
        ][0]['lider']

    # def test_participar_grupo(self):

    #     url = '/grupos/'

    #     response = self.client.post(
    #         url
    #     )

    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_400_BAD_REQUEST
    #     )
    #     self.assertEqual(
    #         str(response.data['aluno'][0]),
    #         'Você não pode criar um grupo sem estar em uma turma.'
    #     )
