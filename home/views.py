import logging
import requests
import requests_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from Robinhood import Robinhood

logger = logging.getLogger('app')

requests_cache.install_cache('rh-requests', backend='sqlite', expire_after=120)


@login_required
@require_http_methods(["GET"])
def v_home(request):
    """
    View  /
    """
    try:
        log_req(request)
        rh = get_rh(request.user.username, request.session['password'])
        securities = get_securities(rh.securities_owned()['results'])
        logger.info(securities)
        return render(request, 'home.html', {'securities': securities})
    except Exception as error:
        logger.exception(error)
        return msg_redirect(
            request, messages.WARNING, 'danger',  'v_error',
            'Error Loading Account Home:<br>{}'.format(error),
        )


def get_securities(securities):
    for s in securities:
        rhs = get_security(s['instrument'])
        s['security'] = rhs
        q = get_quote(s['security']['quote'])
        s['quote'] = q
        # f = get_fundamental(s['security']['fundamentals'])
        # s['fundamentals'] = f
    return securities


def get_security(instrument):
    r = requests.get(instrument)
    if r.status_code == 200:
        return r.json()
    else:
        logger.error(r.content.decode('utf-8'))
        return None


def get_fundamental(fundamental):
    r = requests.get(fundamental)
    if r.status_code == 200:
        return r.json()
    else:
        logger.error(r.content.decode('utf-8'))
        return None


def get_quote(quote):
    r = requests.get(quote)
    if r.status_code == 200:
        return r.json()
    else:
        logger.error(r.content.decode('utf-8'))
        return None


@login_required
@require_http_methods(["GET"])
def v_error(request):
    """
    View  /account/
    """
    return render(request, 'error.html')


def msg_redirect(request, msg_type, tags, location, message):
    messages.add_message(request, msg_type, message, extra_tags=tags)
    return redirect(location)


def get_rh(username, password):
    with requests_cache.disabled():
        rh = Robinhood()
        l = rh.login(
            username=username,
            password=password,
        )
        if l:
            return rh
        else:
            return None


def log_req(request):
    """
    DEBUGGING ONLY
    """
    data = ''
    if request.method == 'GET':
        data = 'GET: '
        for key, value in request.GET.items():
            data += '"%s": "%s", ' % (key, value)
    if request.method == 'POST':
        data = 'POST: '
        for key, value in request.POST.items():
            data += '"%s": "%s", ' % (key, value)
    if data:
        data = data.strip(', ')
        logger.info(data)
        json_string = '{%s}' % data
        return json_string
    else:
        return None
