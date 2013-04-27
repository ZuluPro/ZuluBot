from django.core.exceptions import ValidationError
from sys import path
import config

def validate_family(value):
    try:
        path.append(config.datafilepath('families'))
        __import__('%s_family' % value)
    except ImportError:
        raise ValidationError("Family %s doesn't exist." % value)
    finally:
        path.pop()

def validate_url(value):
    if not value.endswith('/'):
        raise ValidationError("URL must finish by '/'")

