from django.contrib import admin

from apps.usuarios.models import Aluno, Professor


class ProfessorAdmin(admin.ModelAdmin):
    list_display=('codigo', 'email', 'nome')
    search_fields=['codigo', 'email']


class AlunoAdmin(admin.ModelAdmin):
    list_display=('matricula', 'email', 'nome')
    search_fields=['matricula', 'email']


admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
