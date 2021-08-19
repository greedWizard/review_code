from django.core.exceptions import ValidationError


def validate_starts_with_zero(value: str):
    if not value.startswith('0'):
        raise ValidationError('ИНН должен начинаться с нуля!')