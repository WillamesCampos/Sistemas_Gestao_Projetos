from django.contrib import admin

from apps.projetos.models import (
    Projeto, Grupo, Tarefa
)


class ProjetoAdmin(admin.ModelAdmin):
    list_display=('codigo', 'nome', 'tipo')
    search_fields=['codigo', 'nome', 'tipo']


class GrupoAdmin(admin.ModelAdmin):
    list_display=('codigo', 'lider')
    search_fields=['codigo', 'lider']


class TarefaAdmin(admin.ModelAdmin):
    list_display=('codigo', 'nome', 'prazo', 'situacao', 'projeto')
    search_fields=['codigo', 'nome', 'projeto__nome']


admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Tarefa, TarefaAdmin)

# Register your models here.
