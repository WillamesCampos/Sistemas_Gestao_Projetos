from celery import shared_task
from apps.core.mail import enviar_email_cadastro


@shared_task(name='notificar_cadastro_email')
def celery_email_cadastro(assunto, mensagem, email, anexos=[]):
    return enviar_email_cadastro(
        assunto,
        mensagem,
        email
    )
