from django.contrib import admin

from turmas.models import Turma


class TurmaAdmin(admin.ModelAdmin):
    list_display=('codigo', 'nome', 'periodo')
    search_fields=['codigo', 'nome', 'periodo']

admin.site.register(Turma, TurmaAdmin)