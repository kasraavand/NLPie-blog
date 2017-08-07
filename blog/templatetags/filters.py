from django import template
register = template.Library()
from markdown2 import markdown
import re


@register.filter
def render(content):
    result = markdown(content, extras=["code-color"] ,safe_mode=False)
    return result


@register.filter
def strip_code(content):
    return re.sub('<code>\s*|(?:\s*readmore\s*)</code>', '', content)
