from django import forms

COUNTRY_CONFIG = (
    ('uk.xml', 'UK'),
)

class NewSignalSiteForm(forms.Form):
    title = forms.CharField(max_length=200)
    country = forms.ChoiceField(choices=COUNTRY_CONFIG, initial='UK')
