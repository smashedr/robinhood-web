import json
import logging
from django import template
from home.models import SaveData

logger = logging.getLogger('app')
register = template.Library()


@register.filter(name='parse_security')
def parse_security(security):
    s = {
        'symbol': security['security']['symbol'],
        'price': security['average_buy_price'],
        'shares': security['quantity'],
        'last': get_last(security['quote']),
        'class': card_class(security),
        'daily': parse_daily(security),
    }
    return s


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
    if int(cost) == 0:
        return 0
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


def card_class(security):
    last = get_last(security['quote'])
    buy = float(security['average_buy_price'])
    if last >= buy:
        return 'text-white bg-success'
    else:
        return 'text-white bg-danger'


def parse_daily(security):
    close = float(security['quote']['previous_close'])
    last = get_last(security['quote'])
    if last >= close:
        bs_class = 'bg-success'
        text = 'Up Today.'
    else:
        bs_class = 'bg-danger'
        text = 'Down Today.'

    dollar = profit_total(close, last, security['quantity'])
    percent = profit_percent(close, last, security['quantity'])
    daily = {
        'class': 'text-white {}'.format(bs_class),
        'total': dollar,
        'percent': percent,
        'text': text,
    }
    return daily


def get_last(value, decimal=2):
    if 'last_extended_hours_trade_price' in value:
        if value['last_extended_hours_trade_price']:
            return round(
                float(value['last_extended_hours_trade_price']), decimal
            )
    return round(float(value['last_trade_price']), decimal)
