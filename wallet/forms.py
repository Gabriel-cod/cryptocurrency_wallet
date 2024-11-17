from django import forms
from .models import Cryptos

class CryptoModelForm(forms.ModelForm):
    class Meta:
        model = Cryptos
        fields = ['crypto_name', 'acronym']
    
    def clean_acronym(self):
        acronym = str(self.cleaned_data.get('acronym')).upper()
        return acronym
    
    def clean_crypto_name(self):
        crypto_name = str(self.cleaned_data.get('crypto_name')).capitalize()
        return crypto_name
