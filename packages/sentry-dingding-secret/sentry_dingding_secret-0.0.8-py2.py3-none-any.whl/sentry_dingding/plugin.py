# coding: utf-8
import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'ps'
    author_url = 'https://github.com/ps465777545/sentry-dingding'
    version = "0.0.5"
    description = 'Send error counts to DingDing.'
    resource_links = [
        ('Source', 'https://github.com/ps465777545/sentry-dingding'),
        ('Bug Tracker', 'https://github.com/ps465777545/sentry-dingding/issues'),
        ('README', 'https://github.com/ps465777545/sentry-dingding/blob/master/README.md'),
    ]

    slug = 'DingDing'
    title = 'DingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def make_sign(self, secret):
        import time
        import hmac
        import hashlib
        import base64
        import urllib
        if isinstance(secret, unicode):
            secret = secret.encode('utf-8')
        timestamp = long(round(time.time() * 1000))
        secret_enc = bytes(secret).encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.quote_plus(base64.b64encode(hmac_code))
        params = {
            'sign': sign,
            'timestamp': timestamp
        }
        return params

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option('access_token', group.project)
        # secret = self.get_option('secret', group.project)
        # params = self.make_sign(secret)
        send_url = DingTalk_API.format(token=access_token)
        title = u"New alert from {}".format(event.project.slug)

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": u"#### {title} \n > {message} [href]({url})".format(
                    title=title,
                    message=event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.id),
                )
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8"),
            # params=params
        )
