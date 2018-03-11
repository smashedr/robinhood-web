from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from rhweb.shared import parse_bulls, parse_si, parse_cnn, parse_ss, parse_sp
import logging
import requests

logger = logging.getLogger('app')
config = settings.CONFIG


@require_http_methods(['GET'])
def home_view(request):
    """
    View: /stock/
    """
    return render(request, 'stock/home.html')


@require_http_methods(['GET'])
def stock_view(request, symbol=''):
    """
    View: /stock/<symbol>/
    """
    if not symbol:
        message = 'Error parsing stock symbol. Try again...'
        messages.add_message(
            request, messages.WARNING, message, extra_tags='danger'
        )
        return render(request, 'stock/results.html')
    else:
        symbol = symbol.upper()
        stock = {
            'symbol': symbol,
            'tv': {
                'market': get_trading_view_market(symbol),
            },
            'bulls': parse_bulls(symbol),
            'si': parse_si(symbol),
            'cnn': parse_cnn(symbol),
            'ss': parse_ss(symbol),
            'sp': parse_sp(symbol),
        }
        return render(request, 'stock/results.html', {'stock': stock})


@require_http_methods(['POST'])
def stock_search(request):
    """
    View: /stock/search/
    """
    symbol = request.POST.get('symbol').upper()
    if not symbol:
        symbol = 'AMZN'
    return redirect('/stock/{}'.format(symbol))


def get_trading_view_market(symbol):
    url = 'https://www.tradingview.com/symbols/NYSE-{}/'.format(symbol)
    r = requests.head(url, timeout=3)
    if r.status_code == 200:
        return 'NYSE'
    url = 'https://www.tradingview.com/symbols/NASDAQ-{}/'.format(symbol)
    r = requests.head(url, timeout=3)
    if r.status_code == 200:
        return 'NASDAQ'
    return None
