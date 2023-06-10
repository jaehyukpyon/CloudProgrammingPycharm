from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TradeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_name = models.CharField(blank=False, null=False, max_length=20)
    quantity = models.DecimalField(decimal_places=8, max_digits=100)
    price = models.DecimalField(decimal_places=3, max_digits=100)
