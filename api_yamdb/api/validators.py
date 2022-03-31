from django.core.exceptions import ValidationError


def validate_score(value):
    if 0 < value > 10:
        raise ValidationError(
            ('Оценка должна быть от 1 до 10'),
            params={'value': value},
        )

