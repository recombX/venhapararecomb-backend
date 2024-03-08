from django import forms

class XMLForm(forms.Form):
    arquivo_xml = forms.FileField()