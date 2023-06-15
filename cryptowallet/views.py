from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CryptoBalance
from cryptocurrency.models import TradeHistory
from datetime import datetime


def format_datetime(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return None


def index(request):
    if not request.user.is_authenticated:
        print("user가 로그인 되어 있지 않음")
        return redirect("/crypto/")

    all_crypto_balance = CryptoBalance.objects.filter(user=request.user)
    if all_crypto_balance.exists():
        response_data = {}
        all_list = []
        for data in all_crypto_balance:
            temp_data = {
                "cryptoName": data.crypto_name,
                "balance": str(data.balance),
                "krwInvestment": str(data.krw_investment),
                "avgBuyPrice": str(data.avg_buy_price),
                "lastTradeDateTime": format_datetime(data.updated),
            }
            all_list.append(temp_data)
        response_data["cryptoList"] = all_list
        response_data["count"] = all_crypto_balance.count()
    else:
        pass
    return render(request, "wallet/mywallet.html", response_data)


def login_(request):
    if request.method == 'GET':
        return render(request, 'wallet/login.html')

    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        user = authenticate(username=id, password=password)

        if user:
            print('성공적으로 로그인 됨')
            login(request, user)
            return redirect('/crypto/')
        else:
            context = {
                "message": 'login failed',
            }
            return render(request, 'wallet/login.html', context)


def history(request):
    all_history_list = TradeHistory.objects.filter(user=request.user).order_by("-date")
    context = {
        "allHistoryList": all_history_list,
    }
    return render(request, 'wallet/history.html', context)
