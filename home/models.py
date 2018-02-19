from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models


class ShareData(models.Model):
    share_owner = models.CharField(
        'Share Owner', max_length=50, primary_key=True
    )
    share_id = models.CharField(
        'Share ID', max_length=255, default='reserved_fore_future_use'
    )
    generated_at = models.DateTimeField('Data Generated Date', default=now)
    securities = models.TextField('Securities JSON', default='')
