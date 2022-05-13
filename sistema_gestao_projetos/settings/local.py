from .base import *

DEBUG = True

MIDDLEWARE.insert(
    1, 'whitenoise.middleware.WhiteNoiseMiddleware'
)

ALLOWED_HOSTS = [
    'localhost'
]