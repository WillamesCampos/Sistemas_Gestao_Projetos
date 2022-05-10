from rest_framework import status

from apps.usuarios.tests.test_login import TestCore
from apps.turmas.tests.factory.turmas import TurmaAlunoFactory, TurmaFactory
from apps.usuarios.tests.factory.usuarios import ProfessorFactory
from apps.projetos.tests.factory.projetos import ProjetoFactory
from apps.projetos.models import Grupo


class TestGrupoAluno(TestCore):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_criar_grupo(self):

        turma = TurmaFactory(
            professor=self.professor
        )

        ProjetoFactory(
            professor=self.professor
        )

        TurmaAlunoFactory(
            turma=turma,
            aluno=self.aluno
        )

        url = '/grupos/'

        response = self.client.post(
            url
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

        response.data(
            response.status_code,
            status.HTTP_201_CREATED
        )
        assert response.data['participantes'][0]['lider']
