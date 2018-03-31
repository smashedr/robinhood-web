import requests
import logging

logger = logging.getLogger('app')


class Robinhood(object):
    url_auth = 'https://api.robinhood.com/api-token-auth/'
    url_accounts = 'https://api.robinhood.com/accounts/'
    url_positions = 'https://api.robinhood.com/positions/'
    url_quotes = 'https://api.robinhood.com/quotes/'

    def __init__(self, token=None):
        self.token = token
        # self.accounts = {}
        self.positions = {}
        self.securities = {}
        # self.stocks = []
        self.symbols = []
        # self.quotes = []

    def get_token(self, username, password, code=None):
        d = self._make_request(
            self.url_auth,
            username=username,
            password=password,
        )
        if 'mfa_required' in d:
            if d['mfa_required']:
                d.clear()
                d = self._make_request(
                    self.url_auth,
                    username=username,
                    password=password,
                    mfa_code=code
                )
        if 'token' in d:
            self.token = d['token']
            return self.token
        else:
            return False

    def get_securities(self):
        self._get_positions()
        self.securities.clear()
        # self._get_stocks()
        for s in self.positions['results']:
            security = self._make_request(
                s['instrument'],
                token=self.token,
                method='get',
            )
            # s['symbol'] = s['security']['symbol']
            self.securities[security['symbol']] = {
                'security': security,
                'position': s,
            }
            self.symbols.append(security['symbol'])
        # self._get_quotes()
        # for s in self.stocks:
        #     s['quote'] = self._return_quote(s['instrument'])
        # s['security']['fundamentals']
        return self.securities

    # def _return_quote(self, instrument):
    #     for q in self.quotes:
    #         if q['instrument'] == instrument:
    #             return q
    #     return None

    # def _get_quotes(self):
    #     symbols = ','.join(self.symbols)
    #     d = self._make_request(
    #         self.url_quotes,
    #         token=self.token,
    #         method='get',
    #         symbols=symbols,
    #     )
    #     self.quotes = d['results']

    # def _get_stocks(self):
    #     self.stocks.clear()
    #     for s in self.positions['results']:
    #         if s['quantity'] != '0.0000':
    #             self.stocks.append(s)

    # def _get_accounts(self):
    #     self.accounts.clear()
    #     self.accounts = self._make_request(
    #         self.url_accounts,
    #         token=self.token,
    #         method='get',
    #     )

    def _get_positions(self):
        self.positions.clear()
        self.positions = self._make_request(
            self.url_positions,
            token=self.token,
            method='get',
        )

    @staticmethod
    def _make_request(url, token=None, method='post', **kwargs):
        data = {}
        for key, value in kwargs.items():
            if value:
                data[key] = value
        headers = {'Accept': 'application/json'}
        if token:
            headers['Authorization'] = 'Token {}'.format(token)
        if method == 'post':
            r = requests.post(url, data=data, headers=headers)
            # logger.info(r.content.decode())
            return r.json()
        elif method == 'get':
            r = requests.get(url, params=data, headers=headers)
            # logger.info(r.content.decode())
            return r.json()
        else:
            raise ValueError('Unknown method.')
