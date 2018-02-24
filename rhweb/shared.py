from cryptography.fernet import Fernet


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


def gen_key():
    return Fernet.generate_key()


def encode_pw(key, clear):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(clear.encode())


def decode_pw(key, enc):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(enc)
