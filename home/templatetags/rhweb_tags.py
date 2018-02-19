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
