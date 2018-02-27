import logging
import requests
from cryptography.fernet import Fernet
from bs4 import BeautifulSoup

logger = logging.getLogger('app')


def parse_sp(symbol):
    try:
        url = 'https://www.shortpainbot.com/?s={}'.format(symbol)
        r = requests.get(url)
        soup = BeautifulSoup(r.content.decode(), 'html.parser')
        main = soup.find_all('div', attrs={'class':'td-ss-main-content'})
        script = main[0].canvas.find_next('script').text

        sp = {
            'script': script,
        }
        return sp
    except Exception as error:
        logger.exception(error)
        return None


def parse_ss(symbol):
    try:
        url = 'http://shortsqueeze.com/?symbol={}'.format(symbol)
        r = requests.get(url)
        soup = BeautifulSoup(r.content.decode(), 'html.parser')
        short = soup.find(string='Short Percent of Float')
        short_per = short.find_next().text.strip('%').strip()
        short = soup.find(string='Short % Increase / Decrease')
        short_change = short.find_next().text.strip('%').strip()
        short = soup.find(string='Short Interest (Shares Short)')
        short_int = short.find_next().text.strip('%').strip()
        ss = {
            'short_per': short_per,
            'short_change': short_change,
            'short_int': short_int,
        }
        return ss
    except Exception as error:
        logger.exception(error)
        return None


def parse_cnn(symbol):
    try:
        url = 'http://money.cnn.com/quote/forecast/forecast.html?symb={}'.format(
            symbol
        )
        r = requests.get(url)
        soup = BeautifulSoup(r.content.decode(), 'html.parser')
        img = soup.find_all('div', attrs={'id':'wsod_forecasts'})[0].img['src']
        rec = soup.find(string='Analyst Recommendations')
        strptxt = 'Move your mouse over pastmonths for detail'
        recommend = rec.find_next('p').text.strip(strptxt)
        signal = rec.find_next('p').find('span').text
        cnn = {
            'img_url': img,
            'recommend': recommend,
            'signal': signal,
        }
        return cnn
    except Exception as error:
        logger.exception(error)
        return None


def parse_si(symbol):
    try:
        url = 'https://stockinvest.us/technical-analysis/{}'.format(symbol)
        r = requests.get(url)
        soup = BeautifulSoup(r.content.decode(), 'html.parser')
        signal_since = soup.find_all('span', attrs={'class':'badge-lg'})[0]
        signal_txt = signal_since.text.replace('\n', '')
        signal_class = signal_since['class'][2].split('-')[1]
        info_table = soup.find_all('table', attrs={'class':'info-widget-table'})
        short = info_table[0].tr.text.split('\n')[2].split(' ( ')
        evalu = soup.find(string='Evaluation')
        eval_text = evalu.find_parent('div').find('p').text.replace('\n', '')
        si = {
            'signal_txt': signal_txt,
            'signal_class': signal_class,
            'short_percent': short[0],
            'short_date': short[1].split(' ')[0],
            'eval_text': eval_text,
        }
        return si
    except Exception as error:
        logger.exception(error)
        return None


def parse_bulls(symbol):
    try:
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
    except Exception as error:
        logger.exception(error)
        return None


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
