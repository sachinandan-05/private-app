from django import template

from Private.utils import encode_id

register = template.Library()


@register.filter
def encoded_id(value):
    return encode_id(value)
