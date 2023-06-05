from django.shortcuts import render
import pyupbit

# Create your views here.

def get_all_krw_strings():
  all_list = pyupbit.get_tickers(fiat = "KRW")
  return all_list

def index(request):
    return render(request, 'crypto/main.html');
