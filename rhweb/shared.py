import logging
import requests
from cryptography.fernet import Fernet
from bs4 import BeautifulSoup

logger = logging.getLogger('app')


def parse_si(symbol):
    url = 'https://stockinvest.us/technical-analysis/{}'.format(symbol)
    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode(), 'html.parser')
    signal_since = soup.find_all('span', attrs={'class':'badge-lg'})[0]
    signal_txt = signal_since.text.replace('\n', '')
    signal_class = signal_since['class'][2].split('-')[1]

    info_table = soup.find_all('table', attrs={'class':'info-widget-table'})
    short = info_table[0].tr.text.split('\n')[2].split(' ( ')

    evalu = soup.find(string="Evaluation")
    eval_text = evalu.find_parent('div').find('p').text.replace('\n', '')

    si = {
        'signal_txt': signal_txt,
        'signal_class': signal_class,
        'short_percent': short[0],
        'short_date': short[1].split(' ')[0],
        'eval_text': eval_text,
    }
    return si


def parse_bulls(symbol):
    url = ('https://www.americanbulls.com/SignalPage.aspx'
           '?lang=en&Ticker={}').format(symbol)
    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode(), 'html.parser')
    last_signal = soup.body.find(
        'span', attrs={'id':'MainContent_LastSignal'}
    ).decode_contents()
    color = soup.body.find(
        'span', attrs={'id':'MainContent_LastSignal'}
    ).find('font').get('color')
    summary = soup.body.find(
        'div', attrs={'id':'MainContent_signalpagedailycommentarytext'}
    ).decode_contents()
    bulls = {
        'last_signal': last_signal,
        'signal_color': color,
        'summary': summary,
    }
    return bulls


def gen_key():
    return Fernet.generate_key()


def encode_pw(key, clear):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(clear.encode())


def decode_pw(key, enc):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(enc)


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
