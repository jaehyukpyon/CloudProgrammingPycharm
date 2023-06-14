from django.db import models
from django.contrib.auth.models import User


class TradeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_name = models.CharField(blank=False, null=False, max_length=20)
    quantity = models.DecimalField(decimal_places=3, max_digits=100)
    target_price = models.DecimalField(decimal_places=3, max_digits=100)
    total_price = models.DecimalField(decimal_places=3, max_digits=100)
    type = models.CharField(blank=False, null=False, max_length=10)
    date = models.DateTimeField(auto_now_add=True)
