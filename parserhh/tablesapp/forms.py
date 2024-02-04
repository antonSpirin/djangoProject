from django import forms


class searchForm(forms.Form):
    vacancy = forms.CharField(label='Search line')
