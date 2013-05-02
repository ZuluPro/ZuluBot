from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import config
from sys import path


def validate_family(value):
    try:
        path.append(config.datafilepath('families'))
        __import__('%s_family' % value)
    except ImportError:
        raise ValidationError(_("Family %(family)s doesn't exist.") %
            {'family': value}
        )
    finally:
        path.pop()


def validate_url(value):
    if not value.endswith('/'):
        raise ValidationError(_("URL must finish by '/'"))
