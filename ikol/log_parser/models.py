from django.db import models


class Log(models.Model):
    ip = models.CharField('IP', max_length=15)
    log_date = models.DateTimeField('Datetime', auto_now_add=True)
    http_method = models.CharField('HTTP method', max_length=12)
    uri_request = models.TextField('URI', )
    response_code = models.IntegerField('Code', )
    response_len = models.IntegerField('Message length', )
    args = models.TextField('Args', )
    client = models.TextField('Client info', )

