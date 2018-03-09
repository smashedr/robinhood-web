from datetime import datetime
import json
import logging
import requests
import requests_cache
from rhweb.shared import decode_pw, get_next_url
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from home.models import ShareData, SaveData
from rhweb.robinhood import Robinhood

logger = logging.getLogger('app')

requests_cache.install_cache('rh-requests', backend='sqlite', expire_after=120)


@login_required
@require_http_methods(["GET"])
def home_view(request):
    """
    View  /
    """
    try:
        if 'pw_key' not in request.COOKIES:
            logout(request)
            return redirect('show_login')
        _token = decode_pw(
            request.COOKIES['pw_key'].encode(),
            request.session['pw_hash'].encode(),
        )
        rh = Robinhood(token=_token.decode())
        positions = rh.get_positions()
        securities = get_securities(positions['results'])
        account = rh.get_accounts()
        account_number = account['results'][0]['account_number']
        data = {
            'securities': securities,
            'share_id': account_number,
        }
        j = json.dumps(securities)
        ShareData.objects.get_or_create(share_owner=request.user.username)
        s = ShareData.objects.get(share_owner=request.user.username)
        s.securities = j
        s.share_id = account_number
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
def share_view(request, share_id):
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


@require_http_methods(["POST"])
def save_share(request):
    """
    View  /save/
    """
    try:
        save_name = request.POST.get('save-name')
        share_id = request.POST.get('share-id')
        if not save_name or not share_id:
            raise ValueError('Invalid Save Name.')
        s = SaveData.objects.get(save_owner=request.user.username)
        s.saved_shares = '{}' if not s.saved_shares else s.saved_shares
        saved_shares = json.loads(s.saved_shares)
        saved_shares[share_id] = save_name
        s.saved_shares = json.dumps(saved_shares)
        s.save()
        messages.add_message(
            request, messages.SUCCESS,
            'Successfully added {} to favorites.'.format(save_name),
            extra_tags='success',
        )
        return redirect(get_next_url(request))
    except Exception as error:
        logger.exception(error)
        messages.add_message(
            request, messages.WARNING,
            'Error saving: {}'.format(error),
            extra_tags='danger',
        )
        return redirect(get_next_url(request))


def get_securities(securities):
    """
    Loop through securities and create custom dictionary
    """
    for s in securities:
        logger.info(type(s['quantity']))
        if s['quantity'] == '0.0000':
            s['watchlist'] = True
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
    r = requests.get(instrument, timeout=3)
    if r.status_code == 200:
        return r.json()
    else:
        return None

