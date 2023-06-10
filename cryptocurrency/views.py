from django.shortcuts import render
import pyupbit

# Create your views here.

def get_all_krw_strings():
  all_list = pyupbit.get_tickers(fiat = "KRW")
  return all_list

def index(request):
    all_crypto_name_list = get_all_krw_strings()
    print(all_crypto_name_list)

    crypto_name = request.GET.get("crypto_name")
    if crypto_name is None:
        crypto_name = "KRW-BTC"

    print(crypto_name)
    context = {
        "crypto_name": crypto_name,
        "all_crypto_name_list": all_crypto_name_list,
    }
    return render(request, 'crypto/main.html', context)

def buy(request):
    pass
