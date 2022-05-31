from django import template

register = template.Library()

@register.filter
def count(value, arg):
    return value.filter(status=arg).count()