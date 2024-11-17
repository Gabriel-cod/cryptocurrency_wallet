from django.contrib import admin
from .models import Cryptos, Wallet, CryptosValue

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'crypto_name', 'added_at')
    search_fields = ('user', 'crypto_name', 'added_at')

class CryptosAdmin(admin.ModelAdmin):
    list_display = ('crypto_name', 'acronym')
    search_fields = ('crypto_name', 'acronym')

class CryptosValueAdmin(admin.ModelAdmin):
    list_display = ('crypto_name', 'value', 'updated_at')
    search_fields = ('crypto_name', 'value', 'updated_at')
    
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Cryptos, CryptosAdmin)
admin.site.register(CryptosValue, CryptosValueAdmin)
