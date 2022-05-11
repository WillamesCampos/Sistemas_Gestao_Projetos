from sistema_gestao_projetos.settings import (
    EMAIL_HOST_USER
)

from django.core.mail import send_mail


def enviar_email_cadastro(assunto, mensagem, email, anexos=[]):

    send_mail(
        assunto,
        mensagem,
        EMAIL_HOST_USER,
        [email]
    )
