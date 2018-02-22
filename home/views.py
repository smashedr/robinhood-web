from cryptography.fernet import Fernet
from datetime import datetime
import json
import logging
import requests
import requests_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from home.models import ShareData
from Robinhood import Robinhood

logger = logging.getLogger('app')

requests_cache.install_cache('rh-requests', backend='sqlite', expire_after=120)


@login_required
@require_http_methods(["GET"])
def home_view(request):
    """
    View  /
    """
    try:
        _password = decode_pw(
            request.COOKIES['pw_key'].encode(),
            request.session['pw_hash'].encode(),
        )
        rh = get_rh(request.user.username, _password)
        a = rh.get_account()
        securities = get_securities(rh.securities_owned()['results'])
        data = {
            'securities': securities,
            'share_id': a['account_number'],
        }
        j = json.dumps(securities)
        ShareData.objects.get_or_create(share_owner=request.user.username)
        s = ShareData.objects.get(share_owner=request.user.username)
        s.securities = j
        s.share_id = a['account_number']
        s.generated_at = datetime.now()
        s.save()
        return render(request, 'home.html', {'data': data})
    except Exception as error:
        logger.exception(error)
        messages.add_message(
            request, messages.WARNING,
            'Error: {}'.format(error),
            extra_tags='danger',
        )
        return render(request, 'error.html')


@require_http_methods(["GET"])
def v_share(request, share_id):
    """
    View  /share/<share_id>/
    """
    s = ShareData.objects.get(share_id=share_id)
    securities = json.loads(s.securities)
    data = {
        'securities': securities,
        'generated_at': s.generated_at,
        'share_id': share_id,
    }
    return render(request, 'share.html', {'data': data})


def get_securities(securities):
    """
    Loop through securities and create custom dictionary
    """
    for s in securities:
        rhs = get_rh_open(s['instrument'])
        s['security'] = rhs
        q = get_rh_open(s['security']['quote'])
        s['quote'] = q
        # f = get_rh_open(s['security']['fundamentals'])
        # s['fundamentals'] = f
    return securities


def get_rh_open(instrument):
    """
    Query an open Robinhood endpoint for json data
    """
    r = requests.get(instrument)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def get_rh(username, _password):
    """
    Get the Robinhood object from Robinhood
    """
    with requests_cache.disabled():
        rh = Robinhood()
        l = rh.login(
            username=username,
            password=_password,
        )
        if l:
            return rh
        else:
            return None


def decode_pw(key, enc):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(enc)
