from django import forms

class PageForm(forms.Form):
    pagename = forms.CharField(max_length=200)

