from cryptography.fernet import Fernet
import logging
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from home.views import get_rh

logger = logging.getLogger('app')


@require_http_methods(['GET'])
def show_login(request):
    """
    View  /login/
    """
    request.session['login_next_url'] = get_next_url(request)
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
        rh = get_rh(_username, _password)
        if rh:
            if login_user(request, _username):
                key = Fernet.generate_key()
                pw_hash = encode_pw(key, _password)
                request.session['pw_hash'] = pw_hash.decode()
                response = HttpResponseRedirect(get_next_url(request))
                response.set_cookie('pw_key', key.decode())
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


def get_next_url(request):
    """
    Determine 'next' Parameter
    """
    try:
        next_url = request.GET['next']
    except:
        try:
            next_url = request.POST['next']
        except:
            try:
                next_url = request.session['login_next_url']
            except:
                next_url = '/'
    if not next_url:
        next_url = '/'
    if '?next=' in next_url:
        next_url = next_url.split('?next=')[1]
    return next_url


def encode_pw(key, clear):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(clear.encode())
