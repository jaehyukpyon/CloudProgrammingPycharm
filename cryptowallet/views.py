from django.shortcuts import render, redirect
from .models import CryptoBalance
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
        response_data["list"] = all_list
        response_data["count"] = all_crypto_balance.count()
    else:
        pass
    return render(request, "wallet/mywallet.html", response_data)
