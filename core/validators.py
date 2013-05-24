from django.core.exceptions import ValidationError
from wikipedia import Family

def validate_family(value):
    try:
        Family(value)
    except SystemExit:
        raise ValidationError("Family %s doesn't exist." % value)

def validate_url(value):
    if not value.endswith('/'):
        raise ValidationError("URL must finish by '/'")

