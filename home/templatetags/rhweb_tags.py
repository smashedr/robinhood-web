import json
import logging
from django import template
from home.models import SaveData

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


@register.simple_tag(name='profit_total')
def profit_total(price, last, shares, decimal=2):
    p = (float(last) * float(shares)) - (float(price) * float(shares))
    return round(p, decimal)


@register.simple_tag(name='profit_percent')
def profit_percent(price, last, shares, decimal=2):
    cost = (float(price) * float(shares))
    profit = (float(last) * float(shares)) - cost
    if profit > 0:
        percent = round(profit/cost*100, 2)
    elif profit < 0:
        percent = round(-profit/cost*100, 2)
    else:
        percent = 0
    return round(percent, decimal)


@register.simple_tag(name='get_saves')
def get_saves(value):
    s = SaveData.objects.get(save_owner=value)
    saved_shares = json.loads(s.saved_shares)
    return saved_shares if saved_shares else None
