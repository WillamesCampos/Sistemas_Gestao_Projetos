from sistema_gestao_projetos.settings.base import *

DEBUG = False

MIDDLEWARE.insert(
    1, 'whitenoise.middleware.WhiteNoiseMiddleware'
)

ALLOWED_HOSTS = [
    'https://sistemas-gestao-projetos.herokuapp.com/'
]