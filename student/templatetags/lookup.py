# 新規: student/templatetags/lookup.py
from django import template
register = template.Library()

@register.filter
def lookup(dict_obj, key):
    return dict_obj.get(key)
