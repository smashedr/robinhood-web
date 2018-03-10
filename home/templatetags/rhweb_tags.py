import json
import logging
from datetime import datetime
from django import template
from django.utils.timezone import utc
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
        'status': get_status(security['quote'], security['average_buy_price']),
        'daily': parse_daily(security),
    }
    return s


@register.filter(name='time_since')
def time_since(value):
    since = datetime.utcnow().replace(tzinfo=utc) - value
    return convert_time(since.seconds)


@register.filter(name='round_it')
def round_it(value, decimal=2):
    if decimal == 0:
        return int(float(value))
    return round(float(value), decimal)


@register.simple_tag(name='my_multiply')
def my_multiply(value1, value2, decimal=2):
    m = float(value1) * float(value2)
    return '{:,.2f}'.format(m)


@register.simple_tag(name='profit_total')
def profit_total(price, last, shares, decimal=2):
    p = (float(last) * float(shares)) - (float(price) * float(shares))
    return '{:,.2f}'.format(p)


@register.simple_tag(name='profit_percent')
def profit_percent(price, last, shares):
    cost = (float(price) * float(shares))
    if int(cost) == 0:
        return 0
    profit = (float(last) * float(shares)) - cost
    if profit > 0:
        return '{:.2f}'.format(profit/cost*100)
    elif profit < 0:
        return '-{:.2f}'.format(-profit/cost*100)
    else:
        return 0


@register.simple_tag(name='get_saves')
def get_saves(value):
    s = SaveData.objects.get(save_owner=value)
    saved_shares = json.loads(s.saved_shares)
    return saved_shares if saved_shares else None


def parse_daily(security):
    close = float(security['quote']['previous_close'])
    last = get_last(security['quote'])
    dollar = profit_total(close, last, security['quantity'])
    percent = profit_percent(close, last, security['quantity'])
    daily = {
        'status': get_status(security['quote'], close),
        'total': dollar,
        'percent': percent,
    }
    return daily


def get_status(quote, average_buy_price):
    last = get_last(quote)
    buy = float(average_buy_price)
    if last >= buy:
        return {
            'up': 'up',
            'class': 'success',
        }
    else:
        return {
            'up': 'down',
            'class': 'danger',
        }


def get_last(value, decimal=2):
    if 'last_extended_hours_trade_price' in value:
        if value['last_extended_hours_trade_price']:
            return round(
                float(value['last_extended_hours_trade_price']), decimal
            )
    return round(float(value['last_trade_price']), decimal)


def convert_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h < 1:
        o = "%02d minutes %02d seconds" % (m, s)
    else:
        o = "%d hours %02d minutes %02d seconds" % (h, m, s)
    return o
