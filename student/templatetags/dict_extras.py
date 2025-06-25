# student/templatetags/dict_extras.py
from django import template

register = template.Library()

@register.filter
def lookup(dict_obj, key):
    """
    テンプレートで {{ my_dict|lookup:some_key }} のように
    辞書から値を取り出せるようにするフィルター
    """
    try:
        return dict_obj.get(key)
    except Exception:
        return None
