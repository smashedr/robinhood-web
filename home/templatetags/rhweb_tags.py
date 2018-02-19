import logging
from django import template

logger = logging.getLogger('app')
register = template.Library()


@register.filter(name='card_class')
def card_class(security):
    ltp = float(security['quote']['last_trade_price'])
    abp = float(security['average_buy_price'])
    if ltp >= abp:
        return 'text-white bg-success'
    else:
        return 'text-white bg-danger'


@register.filter(name='round_it')
def round_it(value, decimal=2):
    if decimal == 0:
        return int(float(value))
    return round(float(value), decimal)


@register.simple_tag(name='my_multiply')
def my_multiply(value1, value2, decimal=2):
    m = float(value1) * float(value2)
    return round(m, decimal)


@register.simple_tag(name='my_profit')
def my_profit(price, last, shares, decimal=2):
    p = (float(last) * float(shares)) - (float(price) * float(shares))
    return round(p, decimal)
