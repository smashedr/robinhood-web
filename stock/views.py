from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import logging
import requests

logger = logging.getLogger('app')
config = settings.CONFIG


@require_http_methods(['GET'])
def home_view(request):
    """
    View: /stock/
    """
    logger.info('stock_view')
    return redirect('/stock/AMZN')


@require_http_methods(['GET'])
def stock_view(request, symbol=''):
    """
    View: /stock/<symbol>/
    """
    logger.info('stock_view')
    logger.info('symbol: {}'.format(symbol))
    if not symbol:
        message = 'Error parsing stock symbol. Try again...'
        messages.add_message(
            request, messages.WARNING, message, extra_tags='danger'
        )
        return render(request, 'stock.html')
    else:
        stock = {
            'symbol': symbol,
            'tv': {
                'market': get_trading_view_market(symbol)
            },
        }
        logger.info(stock)
        return render(request, 'stock.html', {'stock': stock})


@require_http_methods(['POST'])
def stock_search(request):
    """
    View: /stock/search/
    """
    logger.info('do_search')
    symbol = request.POST.get('symbol').upper()
    logger.info('symbol: {}'.format(symbol))
    if not symbol:
        symbol = 'AMZN'
    return redirect('/stock/{}'.format(symbol))


def get_trading_view_market(symbol):
    url = 'https://www.tradingview.com/symbols/NYSE-{}/'.format(symbol)
    r = requests.head(url)
    if r.status_code == 200:
        return 'NYSE'
    url = 'https://www.tradingview.com/symbols/NASDAQ-{}/'.format(symbol)
    r = requests.head(url)
    if r.status_code == 200:
        return 'NASDAQ'
    return None
