from django.db import models
from django.contrib.auth.models import User


class Cryptos(models.Model):
    crypto_name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=10)
    current_value = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.crypto_name

        
class CryptosValue(models.Model):
    crypto_name = models.ForeignKey(Cryptos, on_delete=models.CASCADE, related_name='value_crypto')
    value = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.value)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallet')
    crypto_name = models.ForeignKey(Cryptos, on_delete=models.PROTECT, related_name='cryptos_wallet')
    current_value = models.FloatField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)
    