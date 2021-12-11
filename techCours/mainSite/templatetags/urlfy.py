from urllib import quote_plus
from django import template

register = template.Library()


@register.filter
def in_course(things, course):
    return things.filter(pk=course)