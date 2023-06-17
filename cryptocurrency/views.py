from django.shortcuts import render
from cryptowallet.models import KRWBalance, CryptoBalance
from .models import TradeHistory
from django.db.models import Q
from django.http import HttpResponse
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from datetime import datetime
import pyupbit
import json


def format_datetime(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return None


def round_to_three_decimal_places(number):
    # 소수점 네 번째 자리에서 반올림해서 소수점 세 번째 자리까지만 반환
    rounded_number = number.quantize(Decimal('0.000'), rounding=ROUND_HALF_UP)
    return rounded_number


def round_down_to_three_decimal_places(number):
    # 소수점 네 번째 자리 이하 싹다 버림
    rounded_number = number.quantize(Decimal('0.000'), rounding=ROUND_DOWN)
    return rounded_number


def round_to_three_decimal_places(number):
    # 소수점 네 번째 자리에서 반올림해서 소수점 세 번째 자리까지만 반환
    rounded_number = number.quantize(Decimal('0.000'), rounding=ROUND_HALF_UP)
    return rounded_number


def get_all_krw_strings():
    all_list = pyupbit.get_tickers(fiat="KRW")
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

    krw_balance = round_down_to_three_decimal_places(get_krw_balance(request.user))
    total_price = request_data.get("totalPrice")
    print("krw_balance: " + str(krw_balance))
    print("total_price: " + str(total_price))
    total_price_decimal = round_down_to_three_decimal_places(Decimal(total_price))

    response_data = {
        'message': 'no message',
    }

    if krw_balance >= total_price_decimal:
        print("매수할 수 있음.")

        # TradeHistory 모델에 트레이드 히스토리를 적립
        quantity = round_down_to_three_decimal_places(Decimal(request_data.get('quantity')))
        target_price = round_down_to_three_decimal_places(Decimal(request_data.get('targetPrice')))
        total_price = round_down_to_three_decimal_places(Decimal(request_data.get('totalPrice')))
        print("quantity: " + str(quantity))
        print("target_price: " + str(target_price))
        print("total_price: " + str(total_price))

        new_trade_history = TradeHistory.objects.create(user=request.user, crypto_name=request_data.get('cryptoName'),
                                                        quantity=quantity, target_price=target_price,
                                                        total_price=total_price, type='buy')

        # 현재 지갑에 해당 코인을 이미 매수했는지 확인하는 작업
        current_balance = get_crypto_balance(request.user, request_data.get('cryptoName'))
        if current_balance > 0:
            print('사용자가 이미 해당 코인을 보유하고 있음.')
            exist_crypto = CryptoBalance.objects.get(
                Q(user=request.user) & Q(crypto_name=request_data.get('cryptoName')))
            added_balance = quantity + exist_crypto.balance
            added_krw_investment = total_price + exist_crypto.krw_investment
            calculated_avg_buy_price = added_krw_investment / added_balance
            exist_crypto.balance = added_balance
            exist_crypto.krw_investment = added_krw_investment
            exist_crypto.avg_buy_price = calculated_avg_buy_price
            exist_crypto.save()
        else:
            print('사용자가 해당 코인을 보유하고 있지 않음.')
            new_crypto = CryptoBalance.objects.create(user=request.user, crypto_name=request_data.get('cryptoName'),
                                                      balance=quantity, krw_investment=total_price,
                                                      avg_buy_price=target_price)

        # 현재 krw잔고에서 구입 구매만큼 빼주기
        new_krw_balance = round_down_to_three_decimal_places(krw_balance - total_price);
        user_krw_balance = KRWBalance.objects.filter(user=request.user).first()
        user_krw_balance.balance = new_krw_balance
        user_krw_balance.save()
        response_data['message'] = 'Buy success.'
        json_data = json.dumps(response_data)
        response = HttpResponse(json_data, content_type='application/json')
        response.status_code = 201
        return response
    else:
        print("매수할 수 없음.")
        response_data['message'] = 'KRW balance is not enough.'
        json_data = json.dumps(response_data)
        response = HttpResponse(json_data, content_type='application/json')
        response.status_code = 402
        return response


def sell(request):
    decoded_data = request.body.decode("utf-8")
    request_data = json.loads(decoded_data)
    print(request_data)

    current_crypto_balance_check = CryptoBalance.objects.filter(
        Q(user=request.user) & Q(crypto_name=request_data.get('cryptoName'))
    )

    if current_crypto_balance_check.exists():
        current_crypto_balance = current_crypto_balance_check.first()
        current_balance = current_crypto_balance.balance
        request_sell_quantity = round_down_to_three_decimal_places(Decimal(request_data.get("quantity")))

        if not request_sell_quantity > current_balance:
            print("매도할 수 있음")
            # 매도 수량 * 단가 계산해서 내 총 krw에 저장
            current_krw_balance = KRWBalance.objects.filter(user=request.user).first()
            current_krw_balance.balance = round_down_to_three_decimal_places(
                current_krw_balance.balance + Decimal(request_data.get("totalPrice")))
            current_crypto_balance.balance = round_down_to_three_decimal_places(
                current_crypto_balance.balance - request_sell_quantity)
            current_crypto_balance.krw_investment = round_down_to_three_decimal_places(
                current_crypto_balance.krw_investment - (current_crypto_balance.avg_buy_price * request_sell_quantity))
            current_krw_balance.save()
            current_crypto_balance.save()
            # TradeHistory
            new_trade_history = TradeHistory.objects.create(user=request.user,
                                                            crypto_name=request_data.get("cryptoName"),
                                                            quantity=request_sell_quantity,
                                                            target_price=Decimal(request_data.get("targetPrice")),
                                                            total_price=Decimal(request_data.get("totalPrice")),
                                                            type="sell")
            response_data = {
                "message": "Sell succeed."
            }
            json_data = json.dumps(response_data)
            response = HttpResponse(json, content_type="application/json")
            response.status_code = 201
            return response
    print("매도할 수 없음")
    response_data = {
        "message": "Balance is not enough for sell."
    }
    json_data = json.dumps(response_data)
    response = HttpResponse(json_data, content_type="application/json")
    response.status_code = 402  # payment required
    return response
