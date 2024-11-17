from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, View, CreateView
from .models import Cryptos, Wallet, CryptosValue
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from cryptocurrencies_api import request_api
from .forms import CryptoModelForm

def get_user_cryptos(user):
    user_cryptos = Wallet.objects.filter(user=user)
    user_cryptos = list(user_cryptos.values())
    user_cryptos = [x['crypto_name_id'] for x in user_cryptos]
    return user_cryptos

def call_api(queryset):
    crypto_list = list()
    for object in queryset:
        crypto_symbol = str(object.acronym).upper().strip()
        crypto_list.append(crypto_symbol)

    for _ in range(5):
        try:
            current_values = request_api.get_current_value(cryptocurrencies=crypto_list)
            if current_values is not None:
                break
        except KeyError:
            continue
    
    for object in queryset:
        crypto_values_instance = CryptosValue.objects.create(crypto_name=object, value=current_values[object.acronym])
        crypto_values_instance.save()


def get_cryptos_value():
    queryset = Cryptos.objects.all()
    cryptos_value_update = CryptosValue.objects.all().first()
    if queryset.first():
        if cryptos_value_update:
            cryptos_value_update = CryptosValue.objects.all().order_by('-updated_at').first()
            now = timezone.now()
            if now and cryptos_value_update.updated_at:
                delta = now - cryptos_value_update.updated_at
                if int(delta.total_seconds()/60) > 5:
                    call_api(queryset=queryset)
        else:
            call_api(queryset=queryset)
            
def update_crypto_values(queryset):
    last_value = CryptosValue.objects.all().order_by('-updated_at').first()
    if last_value:
        last_value = last_value.updated_at
        last_hour = last_value.hour
        last_minute = last_value.minute

        if len(str(last_hour)) < 2:
            last_hour = f'0{last_hour}'
        if len(str(last_minute)) < 2:
            last_minute = f'0{last_minute}'        

        last_datetime = f"{last_value.date()} {last_hour}:{last_minute}"
        values = CryptosValue.objects.all().filter(updated_at__contains=last_datetime)
        for crypto in queryset: 
            for value in values:
                if crypto == value.crypto_name or crypto.crypto_name == value.crypto_name:
                    crypto.current_value = value.value
        return queryset
    
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class WalletListView(ListView):
    model = Wallet
    template_name = 'wallet/home.html'
    context_object_name = 'object'
    
    def get_queryset(self):
        get_cryptos_value()
        queryset = super().get_queryset().filter(user=self.request.user).order_by('crypto_name')
        queryset = update_crypto_values(queryset)
        context = {
            'wallet': queryset
        }
        return context

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CryptoDeleteView(DeleteView):
    model = Wallet
    template_name = 'wallet/confirm_delete.html'
    success_url = '/'

@login_required(login_url='/login/')
def delete_crypto_wallet(request, *args, **kwargs):
    crypto_id = kwargs['pk']
    crypto_instance = Cryptos.objects.filter(pk=crypto_id).first()
    cryptos_user = Wallet.objects.filter(user=request.user)
    delete_crypto_user = cryptos_user.filter(crypto_name=crypto_instance).first()

    return redirect('delete', pk=delete_crypto_user.pk)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CryptocurrenciesListView(ListView):
    model = Cryptos
    template_name = 'wallet/cryptocurrencies.html'
    context_object_name = 'object'
    
    def get_queryset(self):
        get_cryptos_value()
        cryptos = super().get_queryset()
        cryptos = update_crypto_values(cryptos)
        user_cryptos = get_user_cryptos(user=self.request.user)
        context = {
            'cryptos': cryptos,
            'user_cryptos': user_cryptos
        }
        
        return context
    
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AddCryptoToWallet(View):
    def get(self, request, *args, **kwargs):
        user_cryptos = get_user_cryptos(user=self.request.user)
        crypto_id = kwargs['pk']
        crypto_instance = Cryptos.objects.filter(pk=crypto_id).first()
        if not crypto_id in user_cryptos:
            instance_wallet = Wallet.objects.create(user=self.request.user, crypto_name=crypto_instance)
            instance_wallet.save()
        return redirect('cryptocurrencies')
    
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateNewCryptocurrency(CreateView):
    model = Cryptos
    form_class = CryptoModelForm
    success_url = '/cryptocurrencies/'
    template_name = 'wallet/create-crypto.html'
    context_object_name = 'form'
            