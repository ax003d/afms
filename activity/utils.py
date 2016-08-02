# coding: utf-8

import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


EMAIL_SIGNATURE = u'\n\n--------\n这封邮件来自乐去网 afms.sinaapp.com'

logger = logging.getLogger('django.request')


def send_mail(title, message, send_to):
    body = u'%s %s' % (message, EMAIL_SIGNATURE)
    message = EmailMultiAlternatives(
        subject=title.encode('utf-8'), 
        body=body.encode('utf-8'),
        from_email=settings.EMAIL_HOST_USER, 
        to=[send_to])
    try:
        message.send(fail_silently=False)
    except socket.error, e:
        logger.exception('send email error!')
