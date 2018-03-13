import logging
from rhweb.shared import gen_key, encode_pw, get_next_url
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from api.views import do_callback
from home.models import SaveData, ConnectData
from rhweb.robinhood import Robinhood

logger = logging.getLogger('app')


@require_http_methods(['GET'])
def connect_success(request):
    """
    View  /connected/
    """
    if 'is_connected' in request.session:
        if request.session['is_connected']:
            return render(request, 'connected.html')
    return redirect('do_connect')


@require_http_methods(['GET'])
def show_connect(request):
    """
    View  /connect/
    """
    _id = request.GET.get('id')
    if not _id:
        messages.add_message(
            request, messages.WARNING,
            'There was an error processing your request. Please try again.',
            extra_tags='danger',
        )
        return render(request, 'error.html')
    data = {'id': _id}
    return render(request, 'connect.html', {'data': data})


@require_http_methods(['POST'])
def do_connect(request):
    """
    View  /conn/
    """
    try:
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        _id = request.POST.get('id')
        _code = request.POST.get('code')
        rh = Robinhood()
        token = rh.get_token(_username, _password, code=_code)
        if token:
            conn, created = ConnectData.objects.get_or_create(
                conn_id=_id, username=_username
            )
            if created:
                r = do_callback(_id)
                if r.status_code == 200:
                    request.session['is_connected'] = True
                    return redirect('connect_success')
                else:
                    messages.add_message(
                        request, messages.WARNING,
                        'Error: {}'.format(r.content),
                        extra_tags='danger',
                    )
                    return redirect('show_connect')
            else:
                conn.username = _username
                conn.save()
                request.session['is_connected'] = True
                return redirect('connect_success')

        else:
            messages.add_message(
                request, messages.WARNING,
                'Incorrect User/Pass. Please Try Again.',
                extra_tags='danger',
            )
            return redirect('show_connect')
    except Exception as error:
        logger.exception(error)
        messages.add_message(
            request, messages.WARNING,
            'Error: {}'.format(error),
            extra_tags='danger',
        )
        return redirect('show_connect')


@require_http_methods(['GET'])
def show_login(request):
    """
    View  /login/
    """
    request.session['login_next_url'] = get_next_url(request)
    if request.user.is_authenticated:
        return redirect(request.session['login_next_url'])
    else:
        return render(request, 'login.html')


@require_http_methods(['POST'])
def do_logout(request):
    """
    View  /logout/
    """
    next_url = get_next_url(request)
    logout(request)
    request.session['login_next_url'] = next_url
    return redirect(next_url)


@require_http_methods(['POST'])
def do_login(request):
    """
    View  /auth/
    """
    try:
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        _code = request.POST.get('code')
        rh = Robinhood()
        token = rh.get_token(_username, _password, code=_code)
        if token:
            if login_user(request, _username):
                key = gen_key()
                pw_hash = encode_pw(key, token)
                request.session['pw_hash'] = pw_hash.decode()
                response = HttpResponseRedirect(get_next_url(request))
                response.set_cookie('pw_key', key.decode())
                SaveData.objects.get_or_create(save_owner=request.user.username)
                return response
            else:
                raise ValueError('Login failed.')
        else:
            messages.add_message(
                request, messages.WARNING,
                'Incorrect User/Pass. Please Try Again.',
                extra_tags='danger',
            )
            return redirect('show_login')
    except Exception as error:
        logger.exception(error)
        messages.add_message(
            request, messages.WARNING,
            'Error: {}'.format(error),
            extra_tags='danger',
        )
        return redirect('show_login')


def login_user(request, username):
    """
    Login or Create New User
    """
    try:
        user = User.objects.filter(username=username).get()
        login(request, user)
        return True
    except ObjectDoesNotExist:
        user = User.objects.create_user(username)
        user.save()
        login(request, user)
        return True
    except Exception as error:
        logger.exception(error)
        return False
