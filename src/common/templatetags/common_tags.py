import json
from decimal import Decimal
import re

from django import template
from django.utils.safestring import mark_safe
import markdown
from typus import ru_typus

register = template.Library()


@register.simple_tag
def verbose_name(instance, field_name):
    """ Returns verbose_name for a field. """
    return str(ru_typus(instance._meta.get_field(field_name).verbose_name))


@register.filter(is_safe=True)
def replace_n(value):
    if value is not None and isinstance(value, str):
        return value.replace('\n', '<br />')
    else:
        return value


@register.filter
def format_number(number):
    # Приводим число к типу Decimal для точности
    if isinstance(number, float):
        number = Decimal(str(number))

    # Форматируем число
    formatted_number = f"{number:,.2f}".replace(',', ' ').replace('.', ',')
    return formatted_number


@register.filter
def format_number_int(number):
    # Приводим число к типу Decimal для точности
    if isinstance(number, float):
        number = Decimal(str(number))

    # Округляем число до ближайшего целого
    formatted_number = round(number)

    # Форматируем число
    formatted_number = f"{formatted_number:,}".replace(',', ' ')
    return formatted_number


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(is_safe=True)
def replace_comma(value):
    if value is not None:
        return value.replace(',', '.')
    else:
        pass


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.filter(name="typus", is_safe=True)
def typus(value):
    return ru_typus(value)


@register.simple_tag()
def my_set(value):
    return value


@register.filter(name="without_quotes", is_safe=True)
def without_quotes(value):
    if value.startswith('"'):
        value = value[:1]
    else:
        value = value
    if value.endswith('"'):
        value = value[:-1]
    else:
        value = value
    return ru_typus(value)


@register.filter(name="format_phone_to_whatsapp", is_safe=True)
def format_phone_to_whatsapp(phone_number):
    """Преобразует номер телефона в формат 79991234567"""

    if not phone_number:
        return phone_number

    # Удаляем все символы, кроме цифр
    cleaned_number = ''.join([char for char in phone_number if char.isdigit()])
    if cleaned_number.startswith('8'):
        cleaned_number = '7' + cleaned_number[1:]
    elif cleaned_number.startswith('+7'):
        cleaned_number = '7' + cleaned_number[2:]

    return cleaned_number


@register.filter(name="clean_phone", is_safe=True)
def clean_phone(phone_number):
    """ Очиска номера телефона от скобок и пробелов """
    clean_number = phone_number.replace(
        ' ', '').replace('(', '').replace(')', '')
    return clean_number


@register.filter(name='markdown')
def markdown_to_html(text):
    """ Преобразует текст с разметкой Markdown в HTML. """
    if text is None:
        return ''
    return markdown.markdown(text)


@register.filter(name='limb_2')
def add_class_to_li(value):
    """ Заменяет <li> на <li class="mb-2"> """
    return re.sub(r'<li>', r'<li class="mb-2">', value)


@register.filter(name='h4mb_3')
def add_class_to_h4(value):
    """ Заменяет <h4> на <h4 class="text-center fw-bold mb-3"> """
    return re.sub(r'<h4>', r'<h4 class="fw-bold mb-3">', value)
