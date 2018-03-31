from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rhweb.shared import parse_bulls, parse_si, parse_cnn, parse_ss, parse_sp
import logging

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
        symbol = symbol.upper().strip()
        stock = {
            'symbol': symbol,
            'bulls': parse_bulls(symbol),
            'si': parse_si(symbol),
            'cnn': parse_cnn(symbol),
            'ss': parse_ss(symbol),
            'sp': parse_sp(symbol),
        }
        return render(request, 'stock/results.html', {'stock': stock})


@csrf_exempt
@require_http_methods(['POST'])
def stock_search(request):
    """
    View: /stock/search/
    """
    symbol = request.POST.get('symbol').upper().strip()
    if not symbol:
        symbol = 'AMZN'
    return redirect('/stock/{}'.format(symbol))
