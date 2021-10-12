import locale
from django import template

register = template.Library()

@register.simple_tag
def rupiah_format(angka, desimal=2):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format("%.*f", (desimal, angka), True)
    return "Rp. {}".format(rupiah)