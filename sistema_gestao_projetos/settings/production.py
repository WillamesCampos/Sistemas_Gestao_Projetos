import os
from sistema_gestao_projetos.settings.base import *
from dj_database_url import parse as dburl
from decouple import config

DEBUG = False

ALLOWED_HOSTS = [
    'sistemas-gestao-projetos.herokuapp.com',
    '0.0.0.0'
]

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {'default': config('DATABASE_URL', default=default_dburl, cast=dburl), }
