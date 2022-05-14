from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  # use if you support internationalization

def validate_interval(value):
    if value < 0.0:
        raise ValidationError(_('%(value)s must be > 0 '), params={'value': value})