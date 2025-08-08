from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def idr(value):
    return f"Rp {intcomma(value).replace(',', '.')},-"


@register.filter
def intdot(value):
    return f"{intcomma(value).replace(',', '.')}"
