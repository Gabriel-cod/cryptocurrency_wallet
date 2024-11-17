from django.urls import path
from .views import *

urlpatterns = [
    path('', WalletListView.as_view(), name='home'),
    path('delete/<int:pk>', CryptoDeleteView.as_view(), name='delete'),
    path('delete-crypto-wallet/<int:pk>', delete_crypto_wallet, name='delete-crypto-wallet'),
    path('cryptocurrencies/', CryptocurrenciesListView.as_view(), name='cryptocurrencies'),
    path('add-crypto/<int:pk>', AddCryptoToWallet.as_view(), name='add-crypto'),
    path('create-cryptocurrency/', CreateNewCryptocurrency.as_view(), name='create-crypto'),
]