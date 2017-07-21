from django import template
register = template.Library()
from markdown2 import markdown


@register.filter
def render(content):
    result = markdown(content, extras=["code-color"] ,safe_mode=False)
    return result
