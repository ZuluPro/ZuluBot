from django.conf import settings
INSTALLED_APPS = settings.INSTALLED_APPS

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql' or 'oracle'.
        'NAME': '/home/zulu/zulubot.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = INSTALLED_APPS+('debug_toolbar','shell_plus')#,'djcelery')
INTERNAL_IPS = ('127.0.0.1','192.168.100.1')
MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES+('debug_toolbar.middleware.DebugToolbarMiddleware',)

WIKI = {
    'path': '/usr/src/pywikipedia',
}
