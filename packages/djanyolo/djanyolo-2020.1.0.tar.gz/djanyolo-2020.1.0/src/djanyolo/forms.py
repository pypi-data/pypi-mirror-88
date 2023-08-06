from django import forms


class UploadForms(forms.Form):
    image = forms.ImageField()
