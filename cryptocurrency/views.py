from django.shortcuts import render
import pyupbit
from cryptowallet.models import KRWBalance, CryptoBalance
from django.db.models import Q
import json
from django.http import HttpResponse

def get_all_krw_strings():
  all_list = pyupbit.get_tickers(fiat = "KRW")
  return all_list

def get_krw_balance(user):
    target = KRWBalance.objects.filter(user=user).first()
    return target.balance

def get_crypto_balance(user, crypto_name):
    target = CryptoBalance.objects.filter(Q(user=user) & Q(crypto_name=crypto_name))
    if target.exists():
       return target.first().balance
    else:
        return 0

def index(request):
    all_crypto_name_list = get_all_krw_strings()
    print(all_crypto_name_list)

    crypto_name = request.GET.get("crypto_name")
    if crypto_name is None:
        crypto_name = "KRW-BTC"
    print("사용자가 요청한 crpyto_name: " + crypto_name)

    # 로그인 됐으면 cryptowallet 앱의 KRWBalance model을 사용해서 사용자의 한화 잔액 가져오기
    krw_balance = "None"
    if request.user.is_authenticated:
        krw_balance = get_krw_balance(request.user)
    print("현재 로그인 한 사용자가 보유한 한화 잔액(krw):")
    print(krw_balance)

    # 로그인 됐으면 cryptowallet 앱의 CryptoBalance model을 사용해서 사용자의 해당 코인 수량 가져오기
    crypto_balance = 0
    if request.user.is_authenticated:
        crypto_balance = get_crypto_balance(request.user, crypto_name)
    print("현재 로그인 한 사용자가 보유한 " + crypto_name + "의 수량:")
    print(crypto_balance)

    context = {
        "crypto_name": crypto_name,
        "all_crypto_name_list": all_crypto_name_list,
        "krw_balance": krw_balance,
        "crypto_balance": crypto_balance,
    }
    print("---------- end of cryptocurrenty/views/index ----------")
    return render(request, 'crypto/crypto.html', context)

def buy(request):
    print("is user authenticated? " + str(request.user.is_authenticated))
    if not request.user.is_authenticated:
        response_data = {
            "message": "User is not authenticated. Please login first.",
        }
        json_data = json.dumps(response_data)
        response = HttpResponse(json_data, content_type="application/json")
        response.status_code = 403
        return response

    if not request.method == "POST":
        response_data = {
            "message": "GET method is not allowed. Please use POST instead.",
        }
        json_data = json.dumps(response_data)
        response = HttpResponse(json_data, content_type="application/json")
        response.status_code = 405
        return response

    decoded_data = request.body.decode("utf-8")
    request_data = json.loads(decoded_data)
    print(request_data)

    krw_balance = get_krw_balance(request.user)
    total_price = request_data.get("totalPrice")
    print("krw_balance: " + str(krw_balance))
    print("total_price: " + str(total_price))
    if (krw_balance >= total_price):
        print("매수할 수 있음.")
    else:
        pass

    json_data = {
        "test": "Good!!",
    }
    response_data = json.dumps(json_data)

    print("---------- end of cryptocurrenty/views/buy ----------")
    return HttpResponse(response_data, content_type='application/json')
