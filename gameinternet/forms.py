from django import forms


class FindIp(forms.Form):
    ip = forms.CharField(label='ip', max_length=16)


class VictimIp(forms.Form):
    login = forms.CharField(label='user',
                            max_length=10,)
    pw = forms.CharField(label='password', max_length=20)
