from django import forms


class LoginBtc(forms.Form):
    wallet = forms.CharField(label='wallet', max_length=70)
    password = forms.CharField(label='password', max_length=70)


class TransferBtc(forms.Form):
    transf_to_wallet = forms.CharField(label='transfer to', max_length=70)
    value = forms.FloatField()

