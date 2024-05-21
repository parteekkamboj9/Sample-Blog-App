from django import template
from myApp.utils.utils import encrypt_id, decrypt_id

register = template.Library()


@register.simple_tag
def encrypt(value):
    return encrypt_id(value)


@register.simple_tag
def decrypt(value):
    return decrypt_id(value)
