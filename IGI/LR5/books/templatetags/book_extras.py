from django import template

register = template.Library()

@register.filter
def get_item(lst, index):
    try:
        return lst[index]
    except (IndexError, TypeError):
        return 0

@register.filter
def max_value(lst):
    try:
        return max(lst)
    except (ValueError, TypeError):
        return 1 