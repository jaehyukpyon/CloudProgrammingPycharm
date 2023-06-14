from django.db import models
from django.contrib.auth.models import User


class KRWBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.000, decimal_places=3, max_digits=25)


class CryptoBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_name = models.CharField(blank=False, null=False, max_length=10)
    balance = models.DecimalField(decimal_places=3, max_digits=100)  # 코인의 총 수량
    krw_investment = models.DecimalField(decimal_places=3, max_digits=100)  # 원화로 축적된 총 투자금액
    avg_buy_price = models.DecimalField(decimal_places=3, max_digits=100)
    updated = models.DateTimeField(auto_now=True)
