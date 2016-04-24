from django import template

register = template.Library()

@register.filter
def listify(generator):
    return list(generator)

