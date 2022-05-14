import os
from sistema_gestao_projetos.settings.base import *
from dj_database_url import parse as dburl
from decouple import config

DEBUG = False

MIDDLEWARE.insert(
    1, 'whitenoise.middleware.WhiteNoiseMiddleware'
)

ALLOWED_HOSTS = [
    'sistemas-gestao-projetos.herokuapp.com, localhost:8000'
]

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {'default': config('DATABASE_URL', default=default_dburl, cast=dburl), }
