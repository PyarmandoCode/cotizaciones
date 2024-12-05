from django import template

register = template.Library()

# @register.filter(name='replace_comma')
# def replace_comma(value):
#     return value.replace(',', '.')

@register.filter
def replace_comma(value):
    if isinstance(value, str):
        return value.replace(',', '.')
    return str(value).replace(',', '.')