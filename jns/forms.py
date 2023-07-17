from django import forms

class SwitchForm(forms.Form):
    switch = forms.CharField(label='Switch:', max_length=20)