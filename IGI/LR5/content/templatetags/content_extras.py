from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Фильтр для получения значения из словаря по ключу
    Использование: {{ dictionary|get_item:key }}
    """
    try:
        return dictionary.get(int(key))
    except (AttributeError, ValueError):
        return None 