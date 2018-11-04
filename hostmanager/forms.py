from django import forms

import re
from django.core.exceptions import ValidationError


class HostForm(forms.Form):
    hostinstancename = forms.CharField(
                    max_length=100,
                    widget = forms.TextInput(attrs = {'class': 'form-control'})
                )

    hostname = forms.CharField(
                    max_length = 100, disabled = True, required = False,
                    widget = forms.TextInput(attrs = {'class': 'form-control'})
                )

    hostname_hide = forms.CharField(
                    max_length=100,
                    widget = forms.TextInput(attrs = {'style': 'display:none'})
                )

    hostipaddr = forms.CharField(
                    required=False,
                    widget = forms.widgets.Textarea(attrs = {'rows':"6", 'cols':"80"})
                )

    hosttype = forms.TypedChoiceField(
                    choices = [(1, '物理机'), (2, 'ECS'), (3, "KVM")],
                    coerce = lambda x: int(x),
                    widget = forms.widgets.RadioSelect()
                )

    hostdesc = forms.CharField(
                    required=False,
                    widget = forms.widgets.Textarea(attrs = {'rows':"6", 'cols':"80"})
                )

    hoststatus = forms.TypedChoiceField(
                    choices = [(1, '上线'), (2, '下线')],
                    coerce = lambda x: int(x),
                    widget = forms.widgets.RadioSelect()
                )

    def clean_hostipaddr(self):
        str = self.cleaned_data['hostipaddr']

        pattern = re.compile('^\s*\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\s*$')
        for ip in str.split(','):
            match = pattern.match(ip)
            if match == None:
                raise ValidationError('错误的IP地址格式')

        return str

