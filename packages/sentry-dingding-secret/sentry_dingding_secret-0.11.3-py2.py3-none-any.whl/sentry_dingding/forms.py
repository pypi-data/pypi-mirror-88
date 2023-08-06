# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from django import forms


class DingTalkOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='DING TALK WEBHOOK ACCESS_TOKEN'
    )
    secret = forms.CharField(
        max_length=255,
        help_text='钉钉机器人加签secret'
    )
