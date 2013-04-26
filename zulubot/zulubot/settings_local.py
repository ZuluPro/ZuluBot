from django.conf import settings
INSTALLED_APPS = settings.INSTALLED_APPS

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql' or 'oracle'.
        'NAME': '/tmp/zulubot.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Celery - Uncomment the following line to enable
INSTALLED_APPS = INSTALLED_APPS+('djcelery',)
if 'djcelery' in INSTALLED_APPS:
    import djcelery
    djcelery.setup_loader()
    BROKER_URL = 'amqp://guest:guest@localhost:5672/'

# Pywikipedia
WIKI = {
    'language': 'fr',
    'family': 'wiki-eno',
    'nick': 'Anthony MONTHE'
}

# Debug
INSTALLED_APPS = INSTALLED_APPS+('debug_toolbar','shell_plus')
INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES+('debug_toolbar.middleware.DebugToolbarMiddleware',)

