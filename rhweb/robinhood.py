import requests
import logging

logger = logging.getLogger('app')


class Robinhood(object):
    url_auth = 'https://api.robinhood.com/api-token-auth/'
    url_accounts = 'https://api.robinhood.com/accounts/'
    url_positions = 'https://api.robinhood.com/positions/'

    def __init__(self, token=None):
        self.token = token
        self.accounts = None
        self.positions = None
        self.stocks = None

    def get_token(self, username, password, code=None):
        j = self._make_request(
            self.url_auth,
            username=username,
            password=password,
        )
        # logger.info(j)
        if 'mfa_required' in j:
            if j['mfa_required']:
                j = self._make_request(
                    self.url_auth,
                    username=username,
                    password=password,
                    mfa_code=code
                )
        # logger.info(j)
        if 'token' in j:
            self.token = j['token']
            return self.token
        else:
            return False

    def get_stocks(self, refresh=False):
        if refresh:
            self.positions = self._get_positions()
        if not self.positions:
            self.positions = self._get_positions()
        self.stocks = []
        for s in self.positions['results']:
            if s['quantity'] == '0.0000':
                continue
            else:
                self.stocks.append(s)
        return self.stocks

    def get_accounts(self, refresh=False):
        if refresh:
            self.accounts = self._get_accounts()
        if not self.accounts:
            self.accounts = self._get_accounts()
        return self.accounts

    def _get_accounts(self):
        j = self._make_request(
            self.url_accounts,
            token=self.token,
            method='get',
        )
        return j

    def get_positions(self, refresh=False):
        if refresh:
            self.positions = self._get_positions()
        if not self.positions:
            self.positions = self._get_positions()
        return self.positions

    def _get_positions(self):
        j = self._make_request(
            self.url_positions,
            token=self.token,
            method='get',
        )
        return j

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
            # logger.info('r.status_code: {}'.format(r.status_code))
            # logger.info('r.content: {}'.format(r.content))
            return r.json()
        elif method == 'get':
            r = requests.get(url, params=data, headers=headers)
            return r.json()
        else:
            raise ValueError('Unknown method.')
