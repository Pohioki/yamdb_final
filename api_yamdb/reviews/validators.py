import re
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            'Год выпуска не может быть больше текущего.'
        )


def validate_username(value):
    """
    Нельзя использовать имя пользователя me.
    """
    pattern = re.compile(r'^[\w.@+-]+')

    if pattern.fullmatch(value) is None:
        match = re.split(pattern, value)
        symbol = ''.join(match)
        raise ValidationError(f'Некорректные символы в username: {symbol}')
    if value == 'me':
        raise ValidationError('Ник "me" нельзя регистрировать!')
    return value


def validate_slug(value):
    """Валидация полей на недопустимые символы"""
    if len(value) > 50:
        raise ValidationError('Длина ссылки не может превышать 50 символов')
    if re.search(r'^[-a-zA-Z0-9_]+$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в SLUG.'),
            params={'value': value},
        )


def validate_length_name(value):
    """Проверка длины строки имени """
    if len(value) > 255:
        raise ValidationError('Длина имени не может превышать 256 символов')
