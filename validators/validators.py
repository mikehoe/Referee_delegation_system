from django.core.exceptions import ValidationError


def validate_rating(value):
    if value < 0.0 or value > 100.0:
        raise ValidationError('The Rating must be between 0 and 100.')

    if round(value, 1) != value:
        raise ValidationError('The Rating must have at most one decimal place.')
