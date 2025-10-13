from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-&(e#shy(&784t(^9#b(*ann6h4ky#0bdkr82s*_ckf)mcor^5t'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'study_nest',
        'USER': 'faran',
        # 'PASSWORD': 'faranf22',#windows
        'PASSWORD': 'f',#wsl
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public'
        }
    }
}

"""
TODO:
deploy on render.com
docker
"""