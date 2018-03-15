from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models


class ShareData(models.Model):
    share_owner = models.CharField(
        'Share Owner', max_length=50, primary_key=True
    )
    share_id = models.CharField('Share ID', max_length=255)
    generated_at = models.DateTimeField('Data Generated Date', default=now)
    securities = models.TextField('Securities JSON', default='{}')


class SaveData(models.Model):
    save_owner = models.CharField(
        'Save Owner', max_length=50, primary_key=True
    )
    save_id = models.CharField(
        'Save ID', max_length=255, default='reserved_fore_future_use'
    )
    saved_shares = models.TextField('Saved Shares JSON', default='{}')


class ConnectData(models.Model):
    conn_id = models.CharField('Connect ID', max_length=255, primary_key=True)
    username = models.CharField('Robinhood Username', max_length=50)
